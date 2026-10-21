# © 2018 Comunitea - Santi Argüeso <santi@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import calendar
from odoo import fields, models, api, exceptions, _
from dateutil.relativedelta import relativedelta



class CashForecast(models.Model):

    _name = "cash.forecast"

    name = fields.Char('Name', required=True)
    periods = fields.Integer('Number of Periods')
    period_type = fields.Selection(
        selection =[('month', 'Month'),
                    ('week', 'Week'),
                    ('day', 'Day')
        ], string='Type of period', default='month')
    date = fields.Date('Calculation Date', readonly=True)
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company,
        required=True, readonly=True
    )
    payment_mode_ids = fields.Many2many(
        comodel_name='account.payment.mode', string=' Payment Modes',
        relation='cash_forecast_paymente_mode_rel',  copy=True
    )
    previous_inputs = fields.Float('Overdue Inputs', readonly=True,
                                   copy=False)
    previous_input_ids = fields.Many2many(
        comodel_name='account.move.line', string='Overdue Journal items',
        relation='cash_forecast_previous_input_rel', readonly=True, copy=False)
    previous_outputs = fields.Float('Overdue Outputs', readonly=True,
                                    copy=False)
    previous_output_ids = fields.Many2many(
        comodel_name='account.move.line', string='Overdue Journal items',
        relation='cash_forecast_previous_output_rel',
        readonly=True, copy=False
    )
    previous_payment_inputs = fields.Float('Overdue Payment Inputs',
        readonly=True, copy=False)
    previous_payment_input_ids = fields.Many2many(
        comodel_name='account.payment.line',
        string='Overdue Input Payment items',
        relation='cash_forecast_previous_payment_input_rel',
        readonly=True,
        copy=False)
    previous_payment_outputs = fields.Float('Overdue Payment Outputs',
        readonly=True, copy=False)
    previous_payment_output_ids = fields.Many2many(
        comodel_name='account.payment.line',
        string='Overdue Output Payment Items',
        relation='cash_forecast_previous_payment_output_rel',
        readonly=True,
        copy=False)
    previous_balance = fields.Float('Overdue Balance', readonly=True,
                                    copy=False)
    cash_line_ids = fields.One2many('cash.forecast.line', 'forecast_id',
                                    readonly=True, copy=False)


    def delete_forecast_lines(self):
        for forecast in self:
            domain = [('forecast_id', '=', forecast.id)]
            self.env['cash.forecast.line'].search(domain).unlink()
        return

    def unlink(self):
        self.delete_forecast_lines()
        res = super(CashForecast, self).unlink()
        return res

    def _get_liquidity_accounts(self):
        """Accounts whose posted balance is the available cash.

        Besides the cash and bank accounts, it includes the outstanding
        receipts/payments accounts (payments not yet reconciled with the
        statement) and the suspense accounts (statement lines not yet
        reconciled). Both kinds are counted so a statement line pending of
        reconciliation does not duplicate its outstanding payment.
        Using a recordset, an account shared by several roles counts once.
        """
        self.ensure_one()
        company_domain = ('company_id', 'child_of', self.company_id.id)
        accounts = self.env['account.account'].search([
            ('account_type', '=', 'asset_cash'),
            ('company_ids', 'child_of', self.company_id.id),
        ])
        journals = self.env['account.journal'].search([
            company_domain, ('type', 'in', ('bank', 'cash', 'credit'))])
        liquid_journals = journals.filtered(
            lambda j: j.type in ('bank', 'cash'))
        accounts |= liquid_journals.default_account_id
        accounts |= liquid_journals.suspense_account_id
        method_lines = (journals.inbound_payment_method_line_ids
                        | journals.outbound_payment_method_line_ids)
        accounts |= method_lines.payment_account_id
        return accounts

    def get_balance(self, account_ids, date_ini, date_end):
        if not account_ids:
            return 0
        company_ids = self.env['res.company'].search(
            [('id', 'child_of', self.company_id.id)]).ids
        query = """
            SELECT COALESCE(SUM(ml.balance), 0.0)
            FROM account_move_line ml
            WHERE ml.account_id IN %s
                AND ml.date <= %s
                AND ml.parent_state = 'posted'
                AND ml.company_id IN %s
            """
        self.env['account.move.line'].flush_model()
        self.env.cr.execute(
            query, (tuple(account_ids.ids), date_ini, tuple(company_ids)))
        return self.env.cr.fetchone()[0] or 0

    @api.model
    def _get_payment_line(self, type, date_start, date_end,
                          posted_only=False):
        domain = self._get_move_line_domain(
            type, date_start, date_end, posted_only=posted_only)
        move_lines = self.env['account.move.line'].search(domain)
        return move_lines.payment_line_ids.filtered(
            lambda x: x.state != 'cancel')

    @api.model
    def _get_move_line_payment(self, type, date_start, date_end):
        domain = self._get_move_line_domain('payments', date_start, date_end)
        payment_accounts = self._get_payment_mode_accounts(type)
        if payment_accounts:
            domain.append(('account_id', 'in', payment_accounts.ids))
        else:
            domain.append(('id', '=', False))
        move_lines = self.env['account.move.line'].search(domain)
        return move_lines


    def _get_move_line_domain(self, type, date_start, date_end,
                              posted_only=False):
        self.ensure_one()
        move_line_domain = [
            ('company_id', 'child_of', self.company_id.id),
            ('date_maturity', '<=', date_end),
            ('reconciled', '=', False),
            # Drafts are kept in the forecast periods on purpose: they work
            # as manual forecast items. Overdue items must be posted.
            ('parent_state', '=', 'posted') if posted_only
            else ('parent_state', '!=', 'cancel'),
        ]
        if date_start:
            move_line_domain.append(
                ('date_maturity', '>=', date_start)
            )
        if type == 'input':
            move_line_domain.append(
                ('account_id.account_type', '=', 'asset_receivable')
            )
        elif type == 'output':
            move_line_domain.append(
                ('account_id.account_type', '=', 'liability_payable'))
        if self.payment_mode_ids:
            payment_mode_ids = self.payment_mode_ids.mapped('id')
            move_line_domain.append(('payment_mode_id', 'in',
                                     payment_mode_ids))

        return move_line_domain

    def _get_payment_mode_accounts(self, type):
        payment_type = 'inbound' if type == 'input' else 'outbound'
        payment_modes = self.payment_mode_ids or self.env[
            'account.payment.mode'
        ].search([
            ('company_id', '=', self.company_id.id),
            ('payment_type', '=', payment_type),
        ])
        accounts = self.env['account.account']
        method_lines_field = f'{payment_type}_payment_method_line_ids'

        for payment_mode in payment_modes:
            journals = payment_mode.fixed_journal_id | \
                payment_mode.variable_journal_ids
            method_lines = journals[method_lines_field].filtered(
                lambda line, payment_mode=payment_mode:
                line.payment_method_id == payment_mode.payment_method_id
            )
            accounts |= method_lines.mapped('payment_account_id')

        return accounts



    @api.model
    def _get_move_lines(self, type, date_start, date_end, posted_only=False):

        domain = self._get_move_line_domain(
            type, date_start, date_end, posted_only=posted_only)
        move_lines = self.env['account.move.line'].search(domain)
        # Items already in a payment order are forecast as payment lines
        return move_lines.filtered(
            lambda x: not x.payment_line_ids.filtered(
                lambda p: p.state != 'cancel'))


    def _get_cash_forecast_line_vals(self, iter, prevline_id):

        if not prevline_id:
            bank_account_ids = self._get_liquidity_accounts()
            initial_balance = self.get_balance(bank_account_ids, self.date,
                                               False)
            start_date = fields.Date.to_date(self.date)
        else:
            initial_balance = prevline_id.final_balance
            start_date =  fields.Date.to_date(prevline_id.end_date) + \
                          relativedelta(days=+1)
        if self.period_type == 'month':
            last_month_day = calendar.monthrange(start_date.year,
                                                 start_date.month)[1]
            end_date = start_date
            end_date = end_date.replace(
                end_date.year, end_date.month, last_month_day)
        elif self.period_type == 'week':
            start_week = start_date - relativedelta(days=start_date.weekday())
            end_date = start_week + relativedelta(days=+6)
        elif self.period_type == 'day':
            end_date = start_date
        input_ids = self._get_move_lines('input', start_date, end_date)
        inputs = sum(input_ids.mapped('amount_residual'))
        payment_input_ids = self._get_payment_line('input', start_date,
                                                   end_date)
        payment_inputs = sum(payment_input_ids.mapped('amount_currency'))
        output_ids = self._get_move_lines('output', start_date, end_date)
        outputs = sum(output_ids.mapped('amount_residual'))
        payment_output_ids = self._get_payment_line('output', start_date,
                                                   end_date)
        payment_outputs = -1 * sum(payment_output_ids.mapped(
            'amount_currency'))
        period_balance = inputs + outputs + payment_inputs + payment_outputs
        final_balance = initial_balance + period_balance
        vals = {
            'month': start_date.month,
            'start_date': start_date,
            'end_date': end_date,
            'initial_balance': initial_balance,
            'inputs': inputs,
            'outputs': outputs,
            'input_ids':[(6, 0, input_ids.ids)],
            'output_ids': [(6, 0, output_ids.ids)],
            'payment_inputs': payment_inputs,
            'payment_outputs': payment_outputs,
            'payment_input_ids': [(6, 0, payment_input_ids.ids)],
            'payment_output_ids': [(6, 0, payment_output_ids.ids)],
            'period_balance': period_balance,
            'final_balance': final_balance,
        }
        return vals

    def create_lines(self):
        self.ensure_one()
        # Search in the forecast company, whatever the company active in the UI
        self = self.with_company(self.company_id)
        self.delete_forecast_lines()
        self.date = fields.Date.today()
        prev_line = None
        previous_date = fields.Date.to_date(self.date) + \
                        relativedelta(days=-1)
        previous_input_ids = self._get_move_lines(
            'input', False, previous_date, posted_only=True)
        previous_output_ids = self._get_move_lines(
            'output', False, previous_date, posted_only=True)
        previous_payment_input_ids = self._get_payment_line(
            'input', False, previous_date, posted_only=True)
        previous_payment_output_ids = self._get_payment_line(
            'output', False, previous_date, posted_only=True)
        previous_inputs = sum(previous_input_ids.mapped(
            'amount_residual'))
        previous_outputs = sum(previous_output_ids.mapped(
            'amount_residual'))
        previous_payment_inputs = sum(previous_payment_input_ids.mapped(
                'amount_currency'))
        previous_payment_outputs = -1 * sum(previous_payment_output_ids.mapped(
            'amount_currency'))
        previous_balance = previous_inputs + \
                           previous_outputs + \
                           previous_payment_inputs + \
                           previous_payment_outputs
        self.write(
            {
                'previous_input_ids': [(6, 0, previous_input_ids.ids)],
                'previous_output_ids': [(6, 0, previous_output_ids.ids)],
                'previous_payment_input_ids': [(6, 0,
                                            previous_payment_input_ids.ids)],
                'previous_payment_output_ids': [(6, 0,
                                            previous_payment_output_ids.ids)],
                'previous_inputs': previous_inputs,
                'previous_outputs': previous_outputs,
                'previous_payment_inputs': previous_payment_inputs,
                'previous_payment_outputs': previous_payment_outputs,
                'previous_balance': previous_balance

            }
        )
        for iter in range(1, self.periods + 1):
            line_vals = self._get_cash_forecast_line_vals(iter, prev_line)
            line_vals['forecast_id'] = self.id

            prev_line = self.env['cash.forecast.line'].create(line_vals)
        return


    def get_calculated_previous_inputs(self):
        res = self.env.ref('cash_forecast.action_payments').read()[0]
        view = self.env.ref('account_due_list.view_payments_tree')
        res['views'] = [(view.id, 'list')]
        res['domain'] = [('id', 'in', self.previous_input_ids.ids)]
        return res

    def get_calculated_previous_outputs(self):
        res = self.env.ref('cash_forecast.action_payments').read()[0]
        view = self.env.ref('account_due_list.view_payments_tree')
        res['views'] = [(view.id, 'list')]
        res['domain'] = [('id', 'in', self.previous_output_ids.ids)]
        return res

    def get_calculated_previous_payment_inputs(self):
        res = self.env.ref('account_payment_order.account_payment_line_action').read()[0]
        res['domain'] = [('id', 'in', self.previous_payment_input_ids.ids)]
        return res

    def get_calculated_previous_payment_outputs(self):
        res = \
        self.env.ref('account_payment_order.account_payment_line_action').read()[
            0]
        res['domain'] = [('id', 'in', self.previous_payment_output_ids.ids)]
        return res

    def view_all_payment_items(self):
        res = self.env.ref(
            'account_due_list.action_invoice_payments').read()[0]
        return res





class CashForecastLine(models.Model):

    _name = "cash.forecast.line"
    prev_line_id = fields.Many2one('cash.forecast.line', 'Previous Line',
                                  readonly=True)
    month = fields.Integer('Month')
    forecast_id = fields.Many2one('cash.forecast', 'Forecast',
                                  readonly=True)
    initial_balance = fields.Float('Initial Balance')
    period_balance = fields.Float('Period Balance')
    final_balance = fields.Float('Final Balance')
    inputs = fields.Float('Inputs')
    input_ids = fields.Many2many(
        comodel_name='account.move.line', string='Input Journal items',
        relation='cash_forecast_input_lines_rel',
    )
    outputs = fields.Float('Outputs')
    output_ids = fields.Many2many(
        comodel_name='account.move.line', string='Output Journal items',
        relation='cash_forecast_output_lines_rel',
    )
    payment_inputs = fields.Float('Payment Inputs', readonly=True, copy=False)
    payment_input_ids = fields.Many2many(
        comodel_name='account.payment.line', string='Input Payment items',
        relation='cash_forecast_payment_input_line_rel', readonly=True,
        copy=False)
    payment_outputs = fields.Float('Payment Outputs', readonly=True,
                                   copy=False)
    payment_output_ids = fields.Many2many(
        comodel_name='account.payment.line', string='Output Payment items',
        relation='cash_forecast_payment_output_lines_rel', readonly=True,
        copy=False)
    start_date = fields.Date('From', readonly=True)
    end_date = fields.Date('To', readonly=True)

    def get_calculated_inputs(self):
        res = self.env.ref('cash_forecast.action_payments').read()[0]
        view = self.env.ref('account_due_list.view_payments_tree')
        res['views'] = [(view.id, 'list')]
        res['domain'] = [('id', 'in', self.input_ids.ids)]
        return res

    def get_calculated_outputs(self):
        res = self.env.ref('cash_forecast.action_payments').read()[0]
        view = self.env.ref('account_due_list.view_payments_tree')
        res['views'] = [(view.id, 'list')]
        res['domain'] = [('id', 'in', self.output_ids.ids)]
        return res

    def get_calculated_payment_inputs(self):
        res = self.env.ref('account_payment_order.account_payment_line_action').\
            read()[0]
        res['domain'] = [('id', 'in', self.payment_input_ids.ids)]
        return res

    def get_calculated_payment_outputs(self):
        res = self.env.ref('account_payment_order.account_payment_line_action').\
            read()[0]
        res['domain'] = [('id', 'in', self.payment_output_ids.ids)]
        return res
