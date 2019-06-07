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
        default=lambda self: self.env.user.company_id,
        required=True, readonly=True
    )
    payment_mode_ids = fields.Many2many(
        comodel_name='account.payment.mode', string=' Payment Modes',
        relation='cash_forecast_paymente_mode_rel',  copy=True
    )
    previous_inputs = fields.Float('Overdue Inputs', readonly=True,
                                   copy=False,
                                   compute='_compute_previous_inputs')
    previous_input_ids = fields.Many2many(
        comodel_name='account.move.line', string=' Overdue Journal items',
        relation='cash_forecast_previous_input_rel', readonly=True, copy=False
    )
    previous_outputs = fields.Float('Overdue Outputs', readonly=True,
                                    copy=False,
                                    compute = '_compute_previous_outputs'
    )
    previous_output_ids = fields.Many2many(
        comodel_name='account.move.line', string=' Overdue Journal items',
        relation='cash_forecast_previous_output_rel', readonly=True, copy=False
    )
    previous_payment_inputs = fields.Float('Overdue Payment Inputs',
                                readonly=True, copy=False,
                                compute = '_compute_previous_payment_inputs')
    previous_payment_input_ids = fields.Many2many(
        comodel_name='bank.payment.line', string=' Overdue Input Payment items',
        relation='cash_forecast_payment_input_rel', readonly=True, copy=False)
    previous_payment_outputs = fields.Float('Overdue Payment Outputs',
                                readonly=True, copy=False,
                                compute='_compute_previous_payment_outputs')
    previous_payment_output_ids = fields.Many2many(
        comodel_name='bank.payment.line', string=' Overdue Output Payment '
                                                 'items',
        relation='cash_forecast_payment_output_rel', readonly=True, copy=False)
    previous_balance = fields.Float('Overdue Balance', readonly=True,
                                    copy=False,
                                    compute='_compute_previous_balance')
    cash_line_ids = fields.One2many('cash.forecast.line', 'forecast_id',
                                    readonly=True, copy=False)


    @api.multi
    def delete_forecast_lines(self):
        for forecast in self:
            domain = [('forecast_id', '=', forecast.id)]
            self.env['cash.forecast.line'].search(domain).unlink()
        return

    @api.multi
    def unlink(self):
        self.delete_forecast_lines()
        res = super(CashForecast, self).unlink()
        return res

    def get_balance(self, account_ids, date_ini, date_end):
        query = """
            SELECT
                SUM(COALESCE(sub.debit, 0.0)) AS debit,
                SUM(COALESCE(sub.credit, 0.0)) AS credit,
                SUM(COALESCE(sub.balance, 0.0)) AS balance
            FROM
            (
                account_account a
                INNER JOIN
                    account_account_type at ON a.user_type_id = at.id
                INNER JOIN
                    account_move_line ml
                        ON a.id = ml.account_id
                        AND ml.date <= %s
                        AND a.id IN %s
            ) sub
            """
        query_params = ()
        query_params += (
            date_ini,
        )
        query_params += (
            tuple(account_ids.ids),
        )
        self.env.cr.execute(query, query_params)
        res = self.env.cr.fetchall()
        return res[0][2]

    @api.model
    def _get_payment_line(self, type, date_start, date_end):
        if type == 'input':
            account_ids = self.env['account.payment.mode'].search([(
                'payment_type', '=', 'inbound')]).mapped(
                'transfer_account_id'). \
                filtered(lambda x: x.user_type_id.type == 'receivable')
        else:
            account_ids = self.env['account.payment.mode'].search([(
                'payment_type', '=', 'outbound')]).mapped(
                'transfer_account_id'). \
                filtered(lambda x: x.user_type_id.type == 'payable')
        domain = self._get_move_line_domain(
            type, date_start, date_end, account_ids)
        move_lines = self.env['account.move.line'].search(domain)
        move_ids = move_lines.mapped('move_id')
        move_lines_2 = self.env['account.move.line'].search([
            ('move_id', 'in', move_ids.mapped('id')),
            ('id', 'not in', move_lines.mapped('id'))
            ])
        return move_lines_2.mapped('bank_payment_line_id')


    @api.multi
    def _get_move_line_domain(self, type, date_start, date_end, account_ids
    = False):
        self.ensure_one()
        move_line_domain = [
            ('company_id', 'child_of', self.company_id.id),
            ('date_maturity', '<=', date_end),
            ('reconciled', '=', False)
        ]
        if date_start:
            move_line_domain.append(
                ('date_maturity', '>=', date_start)
            )
        if type == 'input':
            move_line_domain.append(
                ('account_id.internal_type', 'in', ('receivable', ))
            )
        elif type== 'output':
            move_line_domain.append(
                ('account_id.internal_type', 'in', ('payable',)))
        if self.payment_mode_ids and not account_ids:
            payment_mode_ids = self.payment_mode_ids.mapped('id')
            move_line_domain.append(('payment_mode_id', 'in',
                                     payment_mode_ids))
        if account_ids:
            move_line_domain.append(('account_id', 'in',
                                    account_ids.mapped('id')))

        return move_line_domain



    @api.model
    def _get_move_lines(self, type, date_start, date_end):

        domain = self._get_move_line_domain(
            type, date_start, date_end)
        return self.env['account.move.line'].search(domain)


    def _get_cash_forecast_line_vals(self, iter, prevline_id):

        if not prevline_id:
            bank_account_ids = self.env['account.account'].search([
                ('user_type_id.type', '=', 'liquidity'),
                ('company_id', 'child_of', self.company_id.id)])
            initial_balance = self.get_balance(bank_account_ids, self.date,
                                               False)
            start_date = fields.Date.from_string(
                        self.date)
        else:
            initial_balance = prevline_id.final_balance
            start_date =  fields.Date.from_string(prevline_id.end_date) + \
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
            'period_balance': period_balance,
            'final_balance': final_balance,
        }
        return vals

    @api.multi
    def create_lines(self):
        self.ensure_one()
        self.delete_forecast_lines()
        self.date = fields.Date.today()
        prev_line = None
        previous_date = fields.Date.from_string(
            self.date) + \
                        relativedelta(days=-1)
        previous_input_ids = self._get_move_lines('input', False,
                                                  previous_date)
        previous_output_ids = self._get_move_lines('output', False,
                                                   previous_date)
        previous_payment_input_ids = self._get_payment_line('input', False,
                                                  previous_date)
        previous_payment_output_ids = self._get_payment_line('output', False,
                                                  previous_date)
        self.write(
            {
                'previous_input_ids': [(6, 0, previous_input_ids.ids)],
                'previous_output_ids': [(6, 0, previous_output_ids.ids)],
                'previous_payment_input_ids': [(6, 0,
                                            previous_payment_input_ids.ids)],
                'previous_payment_output_ids': [(6, 0,
                                            previous_payment_output_ids.ids)],
            }
        )
        for iter in range(1, self.periods + 1):
            line_vals = self._get_cash_forecast_line_vals(iter, prev_line)
            line_vals['forecast_id'] = self.id

            prev_line = self.env['cash.forecast.line'].create(line_vals)
        return

    @api.multi
    @api.depends('previous_input_ids')
    def _compute_previous_inputs(self):
        for forecast in self:
            forecast.previous_inputs = sum(forecast.previous_input_ids.mapped(
                'amount_residual'))

    @api.multi
    @api.depends('previous_output_ids')
    def _compute_previous_outputs(self):
        for forecast in self:
            forecast.previous_outputs = -1 * sum(
                forecast.previous_output_ids.mapped(
                'amount_residual'))

    @api.multi
    @api.depends('previous_payment_input_ids')
    def _compute_previous_payment_inputs(self):
        for forecast in self:
            forecast.previous_payment_inputs = sum(
                forecast.previous_payment_input_ids.mapped(
                'amount_currency'))

    @api.multi
    @api.depends('previous_payment_output_ids')
    def _compute_previous_payment_outputs(self):
        for forecast in self:
            forecast.previous_payment_outputs = sum(
                forecast.previous_payment_output_ids.mapped(
                    'amount_currency'))

    @api.multi
    @api.depends('previous_outputs', 'previous_inputs')
    def _compute_previous_balance(self):
        for forecast in self:
            forecast.previous_balance = forecast.previous_inputs + \
                                        forecast.previous_outputs + \
                                        forecast.previous_payment_inputs + \
                                        forecast.previous_payment_outputs

    def get_calculated_previous_inputs(self):
        res = self.env.ref('cash_forecast.action_payments').read()[0]
        view = self.env.ref('account_due_list.view_payments_tree')
        res['views'] = [(view.id, 'tree')]
        res['domain'] = [('id', 'in', self.previous_input_ids.ids)]
        return res

    def get_calculated_previous_outputs(self):
        res = self.env.ref('cash_forecast.action_payments').read()[0]
        view = self.env.ref('account_due_list.view_payments_tree')
        res['views'] = [(view.id, 'tree')]
        res['domain'] = [('id', 'in', self.previous_output_ids.ids)]
        return res

    def get_calculated_previous_payment_inputs(self):
        res = self.env.ref('account_payment_order.bank_payment_line_action').read()[0]
        res['domain'] = [('id', 'in', self.previous_payment_input_ids.ids)]
        return res

    def get_calculated_previous_payment_outputs(self):
        res = \
        self.env.ref('account_payment_order.bank_payment_line_action').read()[
            0]
        res['domain'] = [('id', 'in', self.previous_payment_output_ids.ids)]
        return res

    def view_forecasted_items(self):
        res = self.env.ref(
            'purchase_advance_payment_forecast.action_forecast_items').read()[0]
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
        comodel_name='account.move.line', string=' Input Journal items',
        relation='cash_forecast_input_lines_rel',
    )
    outputs = fields.Float('Outputs')
    output_ids = fields.Many2many(
        comodel_name='account.move.line', string=' Output Journal items',
        relation='cash_forecast_output_lines_rel',
    )
    payment_inputs = fields.Float('Payment Inputs', readonly=True, copy=False)
    payment_input_ids = fields.Many2many(
        comodel_name='bank.payment.line', string='Input Payment items',
        relation='cash_forecast_payment_input_line_rel', readonly=True,
        copy=False)
    payment_outputs = fields.Float('Payment Outputs', readonly=True,
                                   copy=False)
    payment_output_ids = fields.Many2many(
        comodel_name='bank.payment.line', string=' Output Payment items',
        relation='cash_forecast_payment_output_lines_rel', readonly=True,
        copy=False)
    start_date = fields.Date('From', readonly=True)
    end_date = fields.Date('To', readonly=True)

    def get_calculated_inputs(self):
        res = self.env.ref('cash_forecast.action_payments').read()[0]
        view = self.env.ref('account_due_list.view_payments_tree')
        res['views'] = [(view.id, 'tree')]
        res['domain'] = [('id', 'in', self.input_ids.ids)]
        return res

    def get_calculated_outputs(self):
        res = self.env.ref('cash_forecast.action_payments').read()[0]
        view = self.env.ref('account_due_list.view_payments_tree')
        res['views'] = [(view.id, 'tree')]
        res['domain'] = [('id', 'in', self.output_ids.ids)]
        return res

    def get_calculated_payment_inputs(self):
        res = self.env.ref('account_payment_order.bank_payment_line_action').\
            read()[0]
        res['domain'] = [('id', 'in', self.payment_input_ids.ids)]
        return res

    def get_calculated_payment_outputs(self):
        res = self.env.ref('account_payment_order.bank_payment_line_action').\
            read()[0]
        res['domain'] = [('id', 'in', self.payment_output_ids.ids)]
        return res