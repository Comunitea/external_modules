# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command, fields
from odoo.exceptions import ValidationError
from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountPaymentManualRate(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 1 USD (company currency) = 2 EUR at the payment date
        cls.foreign_currency = cls.setup_other_currency(
            "EUR", rates=[("2016-01-01", 2.0)]
        )
        cls.payment_date = fields.Date.to_date("2017-01-01")
        cls.bank_journal = cls.company_data["default_journal_bank"]

    def _create_payment(self, **kwargs):
        vals = {
            "payment_type": "outbound",
            "partner_type": "supplier",
            "partner_id": self.partner_a.id,
            "amount": 100.0,
            "currency_id": self.foreign_currency.id,
            "date": self.payment_date,
            "journal_id": self.bank_journal.id,
        }
        vals.update(kwargs)
        return self.env["account.payment"].create(vals)

    def _liquidity_balance(self, payment):
        liquidity, counterpart, _writeoff = payment._seek_for_lines()
        return liquidity.balance, counterpart.balance

    def test_system_rate_by_default(self):
        payment = self._create_payment()
        self.assertTrue(payment.manual_rate_available)
        self.assertFalse(payment.use_manual_rate)
        self.assertAlmostEqual(payment.manual_rate, 2.0)
        self.assertAlmostEqual(payment.manual_inverse_rate, 0.5)
        payment.action_validate()
        self.assertEqual(self._liquidity_balance(payment), (-50.0, 50.0))

    def test_manual_rate_on_create(self):
        payment = self._create_payment(manual_rate=4.0)
        self.assertAlmostEqual(payment.manual_inverse_rate, 0.25)
        payment.action_validate()
        self.assertEqual(self._liquidity_balance(payment), (-25.0, 25.0))
        self.assertEqual(payment.amount_company_currency_signed, -25.0)

    def test_manual_inverse_rate_on_create(self):
        payment = self._create_payment(manual_inverse_rate=0.4)
        self.assertAlmostEqual(payment.manual_rate, 2.5)
        payment.action_validate()
        self.assertEqual(self._liquidity_balance(payment), (-40.0, 40.0))

    def test_manual_rate_changed_on_draft_payment(self):
        # An empty write-off list makes Odoo create the draft journal entry
        payment = self._create_payment(write_off_line_vals=[])
        payment.write({"manual_inverse_rate": 0.8})
        self.assertTrue(payment.use_manual_rate)
        self.assertAlmostEqual(payment.manual_rate, 1.25)
        self.assertEqual(self._liquidity_balance(payment), (-80.0, 80.0))
        payment.write({"manual_rate": 5.0})
        self.assertEqual(self._liquidity_balance(payment), (-20.0, 20.0))
        payment.action_refresh_manual_rate()
        self.assertFalse(payment.use_manual_rate)
        self.assertAlmostEqual(payment.manual_rate, 2.0)
        self.assertEqual(self._liquidity_balance(payment), (-50.0, 50.0))

    def test_manual_rate_form(self):
        form = Form(self.env["account.payment"])
        form.payment_type = "outbound"
        form.partner_id = self.partner_a
        form.amount = 100.0
        form.journal_id = self.bank_journal
        form.currency_id = self.foreign_currency
        form.date = self.payment_date
        self.assertAlmostEqual(form.manual_rate, 2.0)
        form.manual_inverse_rate = 0.25
        self.assertAlmostEqual(form.manual_rate, 4.0)
        payment = form.save()
        payment.action_validate()
        self.assertEqual(self._liquidity_balance(payment), (-25.0, 25.0))

    def test_manual_rate_reset_on_currency_change(self):
        form = Form(self.env["account.payment"])
        form.journal_id = self.bank_journal
        form.currency_id = self.foreign_currency
        form.manual_inverse_rate = 0.25
        form.currency_id = self.company_data["currency"]
        self.assertFalse(form.use_manual_rate)
        self.assertFalse(form.manual_rate_available)

    def test_manual_rate_ignored_in_company_currency(self):
        payment = self._create_payment(
            currency_id=self.company_data["currency"].id,
            manual_rate=4.0,
        )
        payment.action_validate()
        self.assertEqual(self._liquidity_balance(payment), (-100.0, 100.0))

    def test_invalid_manual_rate(self):
        with self.assertRaises(ValidationError):
            self._create_payment(manual_rate=-1.0)

    def _create_foreign_bill(self, amount=100.0):
        bill = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": self.payment_date,
                "date": self.payment_date,
                "currency_id": self.foreign_currency.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "line",
                            "quantity": 1,
                            "price_unit": amount,
                            "tax_ids": [],
                        }
                    )
                ],
            }
        )
        bill.action_post()
        return bill

    def _register(self, bill, **vals):
        wizard = self.env["account.payment.register"].with_context(
            active_model="account.move", active_ids=bill.ids
        )
        return wizard.create({"payment_date": self.payment_date, **vals})

    def test_register_payment_manual_rate(self):
        bill = self._create_foreign_bill()
        self.assertEqual(bill.amount_total_signed, -50.0)
        wizard = self._register(bill)
        self.assertTrue(wizard.manual_rate_available)
        self.assertFalse(wizard.use_manual_rate)
        wizard.write({"manual_inverse_rate": 0.6})
        self.assertAlmostEqual(wizard.manual_rate, 1 / 0.6)
        payment = wizard._create_payments()
        self.assertTrue(payment.use_manual_rate)
        self.assertIn(payment.state, ("in_process", "paid"))
        self.assertEqual(self._liquidity_balance(payment), (-60.0, 60.0))
        self.assertEqual(bill.payment_state, "paid")
        # The difference with the bill goes to the exchange difference journal
        exchange_move = bill.line_ids.matched_debit_ids.exchange_move_id
        self.assertTrue(exchange_move)

    def test_register_payment_without_manual_rate(self):
        bill = self._create_foreign_bill()
        payment = self._register(bill)._create_payments()
        self.assertFalse(payment.use_manual_rate)
        self.assertEqual(self._liquidity_balance(payment), (-50.0, 50.0))

    def test_register_payment_manual_rate_partial_with_writeoff(self):
        bill = self._create_foreign_bill()
        writeoff_account = self.company_data["default_account_expense"]
        wizard = self._register(
            bill,
            amount=80.0,
            manual_rate=4.0,
            payment_difference_handling="reconcile",
            writeoff_account_id=writeoff_account.id,
            writeoff_label="Write-off",
        )
        payment = wizard._create_payments()
        liquidity, counterpart, writeoff = payment._seek_for_lines()
        self.assertEqual(liquidity.balance, -20.0)
        self.assertEqual(writeoff.amount_currency, -20.0)
        self.assertEqual(writeoff.balance, -5.0)
        self.assertEqual(counterpart.balance, 25.0)
        self.assertEqual(bill.payment_state, "paid")

    def test_register_payment_manual_rate_ignored_when_grouping_unavailable(self):
        bill = self._create_foreign_bill() | self._create_foreign_bill(200.0)
        wizard = self._register(bill, group_payment=False)
        self.assertFalse(wizard.manual_rate_available)

    def test_register_payment_in_company_currency_manual_rate(self):
        """Pay a bill in a foreign currency with a journal in company currency."""
        bill = self._create_foreign_bill()  # 100 EUR = 50 USD at system rate
        company_currency = self.company_data["currency"]
        wizard = self._register(bill, currency_id=company_currency.id)
        self.assertEqual(wizard.currency_id, company_currency)
        self.assertEqual(wizard.manual_rate_currency_id, self.foreign_currency)
        self.assertTrue(wizard.manual_rate_available)
        self.assertEqual(wizard.amount, 50.0)
        # The rate is the one of the bill currency: 4 EUR per USD
        wizard.write({"manual_rate": 4.0})
        self.assertTrue(wizard.use_manual_rate)
        self.assertEqual(wizard.amount, 25.0)
        self.assertEqual(wizard.payment_difference, 0.0)
        payment = wizard._create_payments()
        # The payment is not affected, the bill is paid at the manual rate
        self.assertFalse(payment.use_manual_rate)
        self.assertEqual(self._liquidity_balance(payment), (-25.0, 25.0))
        self.assertEqual(bill.payment_state, "paid")
        self.assertEqual(bill.amount_residual, 0.0)

    def test_register_payment_in_company_currency_partial_manual_rate(self):
        bill = self._create_foreign_bill()
        company_currency = self.company_data["currency"]
        wizard = self._register(
            bill, currency_id=company_currency.id, amount=10.0, manual_rate=4.0
        )
        payment = wizard._create_payments()
        self.assertEqual(payment.amount, 10.0)
        # 10 USD at 4 EUR per USD
        self.assertEqual(bill.amount_residual, 60.0)
        self.assertEqual(bill.payment_state, "partial")

    def test_register_payment_two_foreign_currencies_no_manual_rate(self):
        other_currency = self.setup_other_currency("CAD", rates=[("2016-01-01", 3.0)])
        bill = self._create_foreign_bill()
        wizard = self._register(bill, currency_id=other_currency.id)
        self.assertFalse(wizard.manual_rate_available)
