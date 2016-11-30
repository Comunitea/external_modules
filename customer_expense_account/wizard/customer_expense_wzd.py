# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from openerp import models, api, fields, _
from openerp.exceptions import except_orm
import time
from ..models.expense_type import COMPUTE_TYPES


class CustomerExpenseWzd(models.TransientModel):
    _name = 'customer.expense.wzd'

    structure_id = fields.Many2one('expense.structure', 'Expense Structure',
                                   required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    company_id = fields.Many2one('res.company', 'Company')

    @api.model
    def default_get(self, fields):
        res = super(CustomerExpenseWzd, self).default_get(fields)
        year = str(time.strftime("%Y"))
        date_start = year + '-' + '01' + '-' + '01'
        date_end = year + '-' + '12' + '-' + '31'

        structure = False
        if self._context.get('active_id', False):
            structure = \
                self.env['res.partner'].browse(self._context['active_id']).\
                structure_id
        res.update(start_date=date_start, end_date=date_end,
                   structure_id=structure.id,
                   company_id=structure.company_id.id)
        return res

    @api.multi
    def action_show_expense(self):
        res = {}
        ctx = self._context.copy()
        ctx.update(from_date=self.start_date, to_date=self.end_date,
                   company_id=self.company_id.id)
        t_expense_line = self.env['expense.line'].with_context(ctx)
        if not self._context.get('active_id', False):
            return res
        partner = self.env['res.partner'].browse(self._context['active_id'])
        line_ids = t_expense_line.get_expense_lines(self.structure_id,
                                                    partner)
        res = {
            'domain': str([('id', 'in', line_ids)]),
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'expense.line',
            'type': 'ir.actions.act_window',
            'nodestroy': True
        }
        return res

    @api.multi
    def action_print_expense(self):
        rep_name = 'customer_expense_account.customer_expense_report'
        rep_action = self.env["report"].get_action(self, rep_name)
        ctx = self._context.copy()
        ctx.update(from_date=self.start_date, to_date=self.end_date,
                   company_id=self.company_id.id)
        t_expense_line = self.env['expense.line'].with_context(ctx)
        p_dic = {}
        for partner in self.env['res.partner'].browse(self._context['active_ids']):
            line_ids = t_expense_line.get_expense_lines(self.structure_id, partner)
            p_dic[partner.id] = line_ids
        custom_data = {'line_objs': p_dic}
        rep_action['data'] = custom_data
        return rep_action


class ExpenseLine(models.TransientModel):
    _name = 'expense.line'

    name = fields.Char('Concept')
    sales = fields.Char('Sales')
    cost = fields.Char('Costs')
    margin = fields.Char('Margin')
    cost_per = fields.Char('% Costs')
    margin_per = fields.Char('% Margin')
    totalizator = fields.Boolean('Totalizator')
    compute_type = fields.Selection(COMPUTE_TYPES, 'Compute Type',
                                    required=True,
                                    readonly=True,
                                    default='analytic')

    @api.model
    def get_expense_lines(self, structure_id, partner):
        line_ids = []
        line_values_lst = self._compute_line_values(partner, structure_id)
        line_ids = self._create_expense_lines(line_values_lst)
        return line_ids

    @api.model
    def _compute_line_values(self, partner, structure):
        res = {}
        values = []
        sales = 0.0
        last_margin = 0.0  # last line
        first = True
        for e in structure.element_ids:
            v = {
                'name': e.name,
                'sales': 0.0,
                'cost': 0.0,
                'margin': 0.0,
                'cost_per': 0.0,
                'margin_per': 0.0,
                'compute_type': e.compute_type
            }
            # Calcule expense amount
            amount = 0.0
            # BASED ON ANALYTIC ACCOUNT
            if e.compute_type == 'analytic':
                amount = self._analytic_compute_amount(e, partner)

            # BASED ON INVOICING
            elif e.compute_type == 'invoicing':
                amount = self._invoicing_compute_amount(e, partner)

            # BASED ON RATIO OVER PARENT ELEMENT
            elif e.compute_type == 'ratio':
                parent_id = e.parent_id.id
                if res.get(parent_id, False):
                    amount = res[parent_id]['cost'] * e.ratio
                    if res[parent_id]['sales']:
                        amount = res[parent_id]['sales'] * e.ratio

            # BASED ON DISTRIBUTION
            elif e.compute_type == 'distribution':
                var_ratio = self._get_var_ratio(partner, e,
                                                e.ratio_compute_type)
                aac = e.expense_type_id.analytic_id
                amount = aac.balance * (-1) * var_ratio

            # BASED ON TOTALIZATOR
            elif e.compute_type in ['total_cost', 'total_margin',
                                    'total_sale']:
                if e.compute_type == 'total_cost':
                    v['cost'] = self._totalizator(values, 'cost')
                    v['cost_per'] = (v['cost'] / (sales or 1.0)) * 100
                elif e.compute_type == 'total_margin':
                    v['margin'] = last_margin
                    v['margin_per'] = (v['margin'] / (sales or 1.0)) * 100
                elif e.compute_type == 'total_sale':
                    v['sales'] = self._totalizator(values, 'sales')
                res[e.id] = v
                values.append(v)
                continue

            # Compute columns
            if amount < 0:  # First time
                if first:
                    first = False
                    v['sales'] = last_margin = sales = amount * (-1)
                else:
                    v['sales'] = amount * (-1)
                    last_margin += v['sales']
                    sales += v['sales']
            else:
                v['cost'] = amount if amount else 0.0

            v['margin'] = last_margin - v['cost']
            v['cost_per'] = (v['cost'] / (sales or 1.0)) * 100
            v['margin_per'] = (v['margin'] / (sales or 1.0)) * 100
            last_margin = v['margin']

            # Adds result to final order list an aux dictionary
            res[e.id] = v
            values.append(v)
        print res
        return values

    def _get_var_ratio(self, partner, e, compute_type):
        res = 0.0
        if compute_type == 'fixed':
            res = e.var_ratio
        elif compute_type == 'invoicing':
            query = self._get_invoice_query(e, False, 'out_invoice')
            self._cr.execute(query)
            qres = self._cr.fetchall()
            q1 = qres[0][0] if qres[0][0] is not None else 0.0

            query = self._get_invoice_query(e, False, 'out_refund')
            self._cr.execute(query)
            qres = self._cr.fetchall()
            q2 = qres[0][0] if qres[0][0] is not None else 0.0
            t1 = q1 - q2

            query = self._get_invoice_query(e, partner, 'out_invoice')
            self._cr.execute(query)
            qres = self._cr.fetchall()
            q1 = qres[0][0] if qres[0][0] is not None else 0.0

            query = self._get_invoice_query(e, partner, 'out_refund')
            self._cr.execute(query)
            qres = self._cr.fetchall()
            q2 = qres[0][0] if qres[0][0] is not None else 0.0
            t2 = q1 - q2
            res = t2 / t1
        return res

    def _analytic_compute_amount(self, e, partner):
        res = 0.0
        query = self._get_analytic_query(e, partner)
        self._cr.execute(query)
        qres = self._cr.fetchall()
        res = qres[0][0] * (-1) if qres[0][0] is not None else 0.0
        return res

    def _invoicing_compute_amount(self, e, partner):
        res = 0.0
        query = self._get_invoice_query(e, partner, 'out_invoice')
        self._cr.execute(query)
        qres = self._cr.fetchall()
        q1 = qres[0][0] if qres[0][0] is not None else 0.0
        query = self._get_invoice_query(e, partner, 'out_refund')
        self._cr.execute(query)
        qres = self._cr.fetchall()
        q2 = qres[0][0] if qres[0][0] is not None else 0.0
        res = q1 - q2
        return res * (-1)

    def _get_invoice_query(self, e, partner, inv_type):
        exp_type = e.expense_type_id
        query = """
            SELECT sum(price_subtotal)
            FROM account_invoice_line ail
            INNER JOIN account_invoice ai ON ai.id = ail.invoice_id
            WHERE ai.date_invoice >= '%s' AND
                  ai.date_invoice <= '%s' AND ai.company_id = %s AND
                  ai.state in ('open', 'paid') AND
                  type = '%s'
        """ % (self._context['from_date'],
               self._context['to_date'], self._context['company_id'], inv_type)
        if partner:
            query += """ AND ai.partner_id = %s """ % str(partner.id)

        if exp_type.product_id:
            query += """ AND ail.product_id = %s """ % exp_type.product_id.id
        elif exp_type.categ_id:
            domain = [('categ_id', 'child_of', exp_type.categ_id.id)]
            prod_objs = self.env['product.product'].search(domain)
            product_ids = [p.id for p in prod_objs]
            if product_ids:
                if len(product_ids) == 1:
                    query += """ AND ail.product_id = %s """ % product_ids[0]
                else:
                    query += """ AND ail.product_id in
                    %s """ % str(tuple(product_ids))
        return query

    def _get_analytic_query(self, e, partner):
        aac = self.env['account.analytic.default'].\
            search([('partner_id', '=', partner.id)], limit=1)
        if not aac:
            return 0.0
        aac = aac.analytic_id
        exp_type = e.expense_type_id
        journal_id = exp_type.journal_id.id if exp_type.journal_id else False

        query = """
            SELECT sum(amount)
            FROM account_analytic_line
            WHERE account_id = %s AND date >= '%s' AND date <= '%s'
              AND company_id = %s
        """ % (str(aac.id), self._context['from_date'],
               self._context['to_date'], e.structure_id.company_id.id)
        if journal_id:
            query += """ AND journal_id = %s """ % str(exp_type.journal_id.id)
        if exp_type.product_id:
            query += """ AND product_id = %s """ % exp_type.product_id.id
        elif exp_type.categ_id:
            domain = [('categ_id', 'child_of', exp_type.categ_id.id)]
            prod_objs = self.env['product.product'].search(domain)
            product_ids = [p.id for p in prod_objs]
            if product_ids:
                if len(product_ids) == 1:
                    query += """ AND product_id = %s """ % product_ids[0]
                else:
                    query += """ AND product_id in
                    %s """ % str(tuple(product_ids))
        return query

    def _totalizator(self, values, key):
        total = 0.0
        for v in values:
            if v['compute_type'] in ['total_cost', 'total_margin',
                                     'total_sale']:
                continue
            total += v[key]
        return total

    @api.model
    def _create_expense_lines(self, line_values):
        res = []
        import locale
        locale.setlocale(locale.LC_ALL, '')
        for v in line_values:
            vals = {
                'name': v['name'],
                'compute_type': v['compute_type'],
                'sales': locale.format("%.2f", round(v['sales'], 2),
                                       grouping=True) if v['sales'] else '',
                'cost': locale.format("%.2f", round(v['cost'], 2),
                                      grouping=True) if v['cost'] else '',
                'margin': locale.format("%.2f", round(v['margin'], 2),
                                        grouping=True) if v['margin'] else '',
                'cost_per':
                    locale.format("%.2f", round(v['cost_per'], 2),
                                  grouping=True) if v['cost_per'] else '',
                'margin_per':
                    locale.format("%.2f", round(v['margin_per'], 2),
                                  grouping=True) if v['margin_per'] else '',
            }
            expense_line = self.create(vals)
            res.append(expense_line.id)
        return res
