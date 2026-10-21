from dateutil.relativedelta import relativedelta

from odoo import Command, fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestCashForecast(TransactionCase):

    def test_create_lines_other_active_company(self):
        """The forecast is computed for its own company, even if the user
        has another one selected in the UI."""
        admin = self.env.ref('base.user_admin')
        company = admin.company_id
        other_company = self.env['res.company'].create({'name': 'Other'})
        admin.company_ids |= other_company
        forecast = self.env['cash.forecast'].with_user(admin).create({
            'name': 'Test', 'periods': 2, 'company_id': company.id,
        })
        forecast = forecast.with_context(
            allowed_company_ids=[other_company.id])
        forecast.create_lines()
        self.assertEqual(len(forecast.cash_line_ids), 2)

    def _create_bill(self, amount, due_date):
        expense = self.env['account.account'].search([
            ('company_ids', 'in', self.env.company.id),
            ('account_type', '=', 'expense'),
        ], limit=1)
        return self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.env['res.partner'].create({'name': 'Vendor'}).id,
            'invoice_date': fields.Date.today(),
            'invoice_date_due': due_date,
            'invoice_line_ids': [Command.create({
                'name': 'Utilities',
                'price_unit': amount,
                'account_id': expense.id,
            })],
        })

    def test_draft_bills_count_but_cancelled_do_not(self):
        due = fields.Date.today() + relativedelta(days=5)
        draft_bill = self._create_bill(100.0, due)
        cancelled_bill = self._create_bill(250.0, due)
        cancelled_bill.button_cancel()
        forecast = self.env['cash.forecast'].create({
            'name': 'Test', 'periods': 1, 'period_type': 'month',
        })
        outputs = forecast._get_move_lines(
            'output', fields.Date.today(), due)
        self.assertTrue(draft_bill.line_ids & outputs)
        self.assertFalse(cancelled_bill.line_ids & outputs)

    def test_overdue_only_posted(self):
        overdue = fields.Date.today() - relativedelta(days=5)
        draft_bill = self._create_bill(100.0, overdue)
        posted_bill = self._create_bill(200.0, overdue)
        posted_bill.action_post()
        forecast = self.env['cash.forecast'].create({
            'name': 'Test', 'periods': 1, 'period_type': 'month',
        })
        forecast.create_lines()
        self.assertFalse(draft_bill.line_ids & forecast.previous_output_ids)
        self.assertTrue(posted_bill.line_ids & forecast.previous_output_ids)

    def _post_entry(self, account, amount, post=True):
        counterpart = self.env['account.account'].search([
            ('company_ids', 'in', self.env.company.id),
            ('account_type', '=', 'expense'),
        ], limit=1)
        journal = self.env['account.journal'].search([
            ('company_id', '=', self.env.company.id),
            ('type', '=', 'general'),
        ], limit=1)
        move = self.env['account.move'].create({
            'move_type': 'entry',
            'journal_id': journal.id,
            'line_ids': [
                Command.create({'account_id': account.id, 'debit': amount}),
                Command.create(
                    {'account_id': counterpart.id, 'credit': amount}),
            ],
        })
        if post:
            move.action_post()
        return move

    def _initial_balance(self, forecast):
        forecast.date = fields.Date.today()
        return forecast._get_cash_forecast_line_vals(1, None)[
            'initial_balance']

    def test_initial_balance_liquidity(self):
        forecast = self.env['cash.forecast'].create({
            'name': 'Test', 'periods': 1, 'period_type': 'month',
        })
        journal = self.env['account.journal'].search([
            ('company_id', '=', self.env.company.id),
            ('type', '=', 'bank'),
        ], limit=1)
        cash = journal.default_account_id
        suspense = journal.suspense_account_id
        outstanding = (
            journal.inbound_payment_method_line_ids.payment_account_id[:1])
        accounts = forecast._get_liquidity_accounts()
        self.assertEqual(len(accounts), len(set(accounts.ids)))
        self.assertIn(cash, accounts)
        self.assertIn(suspense, accounts)
        if not outstanding:
            self.skipTest('The bank journal has no outstanding account')
        self.assertIn(outstanding, accounts)

        base = self._initial_balance(forecast)
        self._post_entry(cash, 100.0, post=False)
        self.assertAlmostEqual(self._initial_balance(forecast), base)
        self._post_entry(cash, 100.0)
        self.assertAlmostEqual(self._initial_balance(forecast), base + 100)
        self._post_entry(outstanding, 40.0)
        self.assertAlmostEqual(self._initial_balance(forecast), base + 140)
        self._post_entry(suspense, -30.0)
        self.assertAlmostEqual(self._initial_balance(forecast), base + 110)

    def test_payment_order_lines_not_counted_twice(self):
        due = fields.Date.today() + relativedelta(days=5)
        bill = self._create_bill(100.0, due)
        bill.action_post()
        payable = bill.line_ids.filtered(
            lambda x: x.account_id.account_type == 'liability_payable')
        method = self.env['account.payment.method'].search([
            ('code', '=', 'sepa_credit_transfer'),
            ('payment_type', '=', 'outbound'),
        ], limit=1)
        mode = self.env['account.payment.mode'].create({
            'name': 'Test transfer',
            'company_id': self.env.company.id,
            'payment_method_id': method.id,
            'bank_account_link': 'variable',
        })
        order = self.env['account.payment.order'].create({
            'payment_mode_id': mode.id,
            'payment_type': 'outbound',
        })
        payment_line = self.env['account.payment.line'].create({
            'order_id': order.id,
            'partner_id': bill.partner_id.id,
            'currency_id': bill.currency_id.id,
            'move_line_id': payable.id,
            'amount_currency': 100.0,
            'communication_type': 'normal',
        })
        forecast = self.env['cash.forecast'].create({
            'name': 'Test', 'periods': 1, 'period_type': 'month',
        })
        today = fields.Date.today()
        self.assertFalse(
            payable & forecast._get_move_lines('output', today, due))
        self.assertEqual(
            forecast._get_payment_line('output', today, due), payment_line)
