# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from openerp import models, api, fields, _
from openerp.exceptions import except_orm
import time


class CustomerExpenseWzd(models.TransientModel):
    _name = 'customer.expense.wzd'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    @api.model
    def default_get(self, fields):
        res = super(CustomerExpenseWzd, self).default_get(fields)
        year = str(time.strftime("%Y"))
        date_start = year + '-' + '01' + '-' + '01'
        date_end = year + '-' + '12' + '-' + '12'
        res.update(start_date=date_start, end_date=date_end)
        return res

    @api.multi
    def action_show_expense(self):
        value = self.env['expense.line'].show_expense_lines(self.start_date,
                                                            self.end_date)
        return value


class ExpenseLine(models.TransientModel):
    _name = 'expense.line'

    name = fields.Char('Concept')
    sales = fields.Float('Sales')
    cost = fields.Float('Costs')
    margin = fields.Float('Margin')
    cost_per = fields.Float('% Costs')
    margin_per = fields.Float('% Margin')

    @api.model
    def show_expense_lines(self, date_start, date_end):
        line_ids = line_values = []
        res = {}
        if not self._context.get('active_id', False):
            return res
        partner = self.env['res.partner'].browse(self._context['active_id'])
        if not partner.structure_id:
            raise except_orm(_('Error'), ('No expense structure founded.'))

        line_values_lst = self._compute_line_values(partner, date_start,
                                                    date_end)
        line_ids = self._create_expense_lines(line_values_lst)
        res = {
            'domain': str([('id', 'in', line_ids)]),
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'expense.line',
            'type': 'ir.actions.act_window',
            'nodestroy': True
        }
        return res

    @api.model
    def _compute_line_values(self, partner, start_date, end_date):
        res = []
        sales = 0.0
        last_margin = 0.0  # last line
        for e in partner.structure_id.element_ids:
            v = [e.expense_type_id.name, 0.0, 0.0, 0.0, 0.0, 0.0]
            if e.expense_type_id.compute_type == 'analytic':
                aac = self.env['account.analytic.account'].\
                    search([('partner_id', '=', partner.id)], limit=1)
                if not aac:
                    continue
                    # raise except_orm(_('Error'),
                    #                  ('No Analytic account founded.'))

                journal_id = e.expense_type_id.journal_id.id
                query = """
                select sum(amount) from account_analytic_line
                where journal_id = %s and account_id = %s and date >= '%s' and
                      date <= '%s'
                """ % (str(journal_id), str(aac.id), start_date, end_date)
                self._cr.execute(query)
                qres = self._cr.fetchall()
                if not qres:
                    continue
                print "QRES "
                print qres
                amount = qres[0][0] if qres[0][0] is not None else 0.0
                if not res:  # First time
                    v[1] = last_margin = sales = amount
                else:
                    v[2] = amount * (-1) if amount else 0.0

                if last_margin:
                    v[3] = last_margin - v[2]
                    v[4] = (v[2] / sales or 1.0) * 100
                    v[5] = (v[3] / sales or 1.0) * 100
                last_margin = v[3]
                res.append(v)
        return res

    @api.model
    def _create_expense_lines(self, line_values):
        res = []
        for v in line_values:
            vals = {
                'name': v[0],
                'sales': round(v[1], 2),
                'cost': round(v[2], 2),
                'margin': round(v[3], 2),
                'cost_per': round(v[4], 2),
                'margin_per': round(v[5], 2),
            }
            expense_line = self.create(vals)
            res.append(expense_line.id)
        return res
