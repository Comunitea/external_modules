# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command, fields
from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestPurchaseAdvancePaymentManualRate(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        if not cls.env.company.chart_template:
            cls.env["account.chart.template"].try_loading(
                "generic_coa", company=cls.env.company, install_demo=False
            )
        cls.company_currency = cls.env.company.currency_id
        cls.foreign_currency = cls.setup_other_currency(
            "EUR" if cls.company_currency.name != "EUR" else "USD",
            rates=[("2000-01-01", 2.0)],
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Foreign Bank",
                "type": "bank",
                "code": "FBNK",
                "currency_id": cls.foreign_currency.id,
            }
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "purchase_advance_payment.auto_post_advance_payments", True
        )
        cls.partner = cls.env["res.partner"].create({"name": "Vendor"})
        cls.product = cls.env["product.product"].create({"name": "Product"})
        cls.order = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner.id,
                "currency_id": cls.company_currency.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "product_qty": 1,
                            "price_unit": 1000.0,
                            "tax_ids": [],
                        }
                    )
                ],
            }
        )

    def _wizard(self, **vals):
        return (
            self.env["account.voucher.wizard.purchase"]
            .with_context(active_ids=self.order.ids, active_id=self.order.id)
            .create(
                {
                    "order_id": self.order.id,
                    "journal_id": self.journal.id,
                    "amount_advance": 100.0,
                    "date": fields.Date.today(),
                    **vals,
                }
            )
        )

    def test_advance_payment_system_rate(self):
        wizard = self._wizard()
        self.assertTrue(wizard.manual_rate_available)
        self.assertFalse(wizard.use_manual_rate)
        # 1 company currency = 2 foreign: 100 foreign are 50 in the order
        self.assertAlmostEqual(wizard.manual_rate, 0.5)
        self.assertAlmostEqual(wizard.currency_amount, 50.0)
        wizard.make_advance_payment()
        payment = self.order.account_payment_ids
        self.assertFalse(payment.use_manual_rate)
        self.assertEqual(sorted(payment.move_id.line_ids.mapped("balance")), [-50.0, 50.0])

    def test_advance_payment_manual_rate(self):
        wizard = self._wizard(manual_rate=0.8)
        self.assertAlmostEqual(wizard.manual_inverse_rate, 1.25)
        self.assertAlmostEqual(wizard.currency_amount, 80.0)
        wizard.make_advance_payment()
        payment = self.order.account_payment_ids
        self.assertTrue(payment.use_manual_rate)
        self.assertAlmostEqual(payment.manual_rate, 1.25)
        self.assertAlmostEqual(payment.manual_inverse_rate, 0.8)
        balances = sorted(payment.move_id.line_ids.mapped("balance"))
        self.assertEqual(balances, [-80.0, 80.0])
        self.assertEqual(self.order.amount_residual, 920.0)
        self.assertEqual(self.order.advance_payment_status, "partial")

    def test_advance_payment_company_currency_journal_foreign_order(self):
        order = self.order.copy({"currency_id": self.foreign_currency.id})
        order.order_line.price_unit = 1000.0
        journal = self.env["account.journal"].search(
            [
                ("type", "=", "bank"),
                ("company_id", "=", self.env.company.id),
                ("currency_id", "=", False),
            ],
            limit=1,
        )
        wizard = (
            self.env["account.voucher.wizard.purchase"]
            .with_context(active_ids=order.ids, active_id=order.id)
            .create(
                {
                    "order_id": order.id,
                    "journal_id": journal.id,
                    "amount_advance": 100.0,
                    "date": fields.Date.today(),
                }
            )
        )
        # The rate is offered to express the advance in the order currency
        self.assertTrue(wizard.manual_rate_available)
        self.assertAlmostEqual(wizard.currency_amount, 200.0)
        self.assertAlmostEqual(wizard.manual_rate, 2.0)
        wizard.write({"manual_rate": 4.0})
        self.assertAlmostEqual(wizard.currency_amount, 400.0)
        wizard.make_advance_payment()
        payment = order.account_payment_ids
        # The payment is made in the order currency, but it takes exactly the
        # amount of the journal from the bank
        self.assertEqual(payment.currency_id, self.foreign_currency)
        self.assertAlmostEqual(payment.amount, 400.0)
        self.assertAlmostEqual(payment.manual_rate, 4.0)
        self.assertEqual(
            sorted(payment.move_id.line_ids.mapped("balance")), [-100.0, 100.0]
        )
        self.assertEqual(
            sorted(payment.move_id.line_ids.mapped("amount_currency")),
            [-400.0, 400.0],
        )
        self.assertAlmostEqual(order.amount_residual, order.amount_total - 400.0)

    def test_advance_payment_manual_rate_without_journal_entry(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "purchase_advance_payment.auto_post_advance_payments", False
        )
        self._wizard(manual_rate=0.8).make_advance_payment()
        payment = self.order.account_payment_ids
        # Simulate the payments without journal entry
        payment.outstanding_account_id = False
        payment.action_post()
        self.assertFalse(payment.move_id)
        self.assertEqual(self.order.amount_residual, 920.0)

    def test_advance_payment_reconciled_with_manual_rate(self):
        """Advance in company currency for an order in a foreign currency."""
        order = self.order.copy({"currency_id": self.foreign_currency.id})
        order.order_line.price_unit = 1000.0
        journal = self.env["account.journal"].search(
            [
                ("type", "=", "bank"),
                ("company_id", "=", self.env.company.id),
                ("currency_id", "=", False),
            ],
            limit=1,
        )
        wizard = (
            self.env["account.voucher.wizard.purchase"]
            .with_context(active_ids=order.ids, active_id=order.id)
            .create(
                {
                    "order_id": order.id,
                    "journal_id": journal.id,
                    "amount_advance": 100.0,
                    "manual_rate": 4.0,
                    "date": fields.Date.today(),
                }
            )
        )
        wizard.make_advance_payment()
        payment = order.account_payment_ids
        self.assertEqual(payment.state, "in_process")
        bill = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": order.partner_id.id,
                "invoice_date": fields.Date.today(),
                "currency_id": self.foreign_currency.id,
                "invoice_line_ids": [
                    Command.create(
                        {"name": "line", "quantity": 1, "price_unit": 1000.0}
                    )
                ],
            }
        )
        bill.action_post()
        # The advance is 400 in the order currency
        content = bill.invoice_outstanding_credits_debits_widget["content"]
        self.assertEqual(len(content), 1)
        self.assertAlmostEqual(content[0]["amount"], 400.0)
        bill.js_assign_outstanding_line(content[0]["id"])
        self.assertAlmostEqual(bill.amount_residual, 600.0)
        self.assertEqual(bill.payment_state, "partial")

    def test_advance_payment_two_foreign_currencies_no_manual_rate(self):
        other_currency = self.setup_other_currency(
            "CAD" if self.foreign_currency.name != "CAD" else "GBP",
            rates=[("2000-01-01", 3.0)],
        )
        order = self.order.copy({"currency_id": other_currency.id})
        wizard = self._wizard(order_id=order.id, currency_id=other_currency.id)
        self.assertFalse(wizard.manual_rate_available)
