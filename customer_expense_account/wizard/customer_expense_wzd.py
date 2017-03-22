# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# © 2017 El Nogal  - Pedro Gómez <pegomez@elnogal.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields, _
from datetime import datetime
import time
from ..models.expense_type import COMPUTE_TYPES


class CustomerExpenseWzd(models.TransientModel):
    _name = 'customer.expense.wzd'

    structure_id = fields.Many2one('expense.structure', 'Expense Structure',
                                   required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    company_id = fields.Many2one('res.company', 'Company')
    use_partner_structure = fields.Boolean('Use customer structure', 
            help='The structure established in the customer will be used. '
            'If the customer does not have any, the selected in the wizard will be applied.')
    only_summary = fields.Boolean('Print summary only',
            help='Print only the summary of the report.')
    summary_description = fields.Char('Summary description')

    @api.model
    def default_get(self, fields):
        res = super(CustomerExpenseWzd, self).default_get(fields)
        year = str(time.strftime("%Y"))
        date_start = year + '-' + '01' + '-' + '01'
        date_end = year + '-' + '12' + '-' + '31'
        structure = False
        model = self._context.get('active_model')
        if self._context.get('active_id', False):
            if self._context.get('all_company', False):
                structure = \
                    self.env[model].browse(self._context['active_id']).\
                    partner_id.structure_id
            else:
                structure = \
                    self.env[model].browse(self._context['active_id']).\
                    structure_id
                structure = structure or \
                    self.env[model].browse(self._context['active_id']).\
                    commercial_partner_id.structure_id
        res.update(start_date=date_start, end_date=date_end,
                   structure_id=structure.id if structure else False,
                   company_id=structure.company_id.id if structure else False)
        return res

    @api.multi
    def action_show_expense(self):
        res = {}
        ctx = self._context.copy()
        ctx.update(from_date=self.start_date, to_date=self.end_date)
        t_expense_line = self.env['expense.line'].with_context(ctx)
        t_partner = self.env['res.partner']
        t_company = self.env['res.company']
        if not self._context.get('active_id', False):
            return res
        if self._context.get('all_company', False):
            partner_ids = [t_company.browse(self._context['active_id']).\
                           partner_id]
            line_ids = t_expense_line.get_expense_lines(self.structure_id, False)
        else:
            partner_ids = [partner.commercial_partner_id
                for partner in t_partner.browse(self._context['active_ids'])
                if partner.commercial_partner_id]
            partner_ids = list(set(partner_ids))
            line_ids = t_expense_line.get_expense_lines(self.structure_id, partner_ids)
        date_from = datetime.strptime(
                    self.start_date, "%Y-%m-%d").strftime('%d-%m-%Y')
        date_to = datetime.strptime(
                    self.end_date, "%Y-%m-%d").strftime('%d-%m-%Y')
        partner_name = partner_ids[0].name if len(partner_ids) == 1 \
                else _("Summary-> %s") % (self.summary_description or '')
        view_name = _("%s (from: %s, to: %s)") \
                    % (partner_name, date_from, date_to)
        res = {
            'domain': str([('id', 'in', line_ids)]),
            'name': view_name,
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'expense.line',
            'type': 'ir.actions.act_window',
            'nodestroy': True
        }
        return res

    @api.multi
    def action_print_expense(self):
        ctx = self._context.copy()
        ctx.update(from_date=self.start_date, to_date=self.end_date)
        t_expense_line = self.env['expense.line'].with_context(ctx)
        t_partner = self.env['res.partner']
        t_company = self.env['res.company']
        p_dic = {}
        if self._context.get('all_company', False):
            partner_ids = [t_company.browse(self._context['active_id']).\
                           partner_id]
        else:
            partner_ids = [partner.commercial_partner_id
                for partner in t_partner.browse(self._context['active_ids'])
                if partner.commercial_partner_id]
            partner_ids = list(set(partner_ids))
        use_partner_structure = self.use_partner_structure \
                                if len(partner_ids) > 1 else False
        if self._context.get('all_company', False):
            structure = self.structure_id
            line_ids = t_expense_line.get_expense_lines(structure, False)
            p_dic[partner_ids[0].id] = (structure.name, line_ids)
        else:
            if not self.only_summary:
                for partner in partner_ids:
                    structure = use_partner_structure and partner.structure_id or \
                                self.structure_id
                    line_ids = t_expense_line.get_expense_lines(structure, partner)
                    p_dic[partner.id] = (structure.name, line_ids)
            if len(partner_ids) > 1: # Summary
                structure = self.structure_id
                line_ids = t_expense_line.get_expense_lines(structure, partner_ids)
                p_dic['summary'] = (structure.name, line_ids)
        custom_data = {'lines_dic': p_dic,
                       'start_date': self.start_date,
                       'end_date': self.end_date,
                       'summary_description': self.summary_description}
        rep_name = 'customer_expense_account.customer_expense_report'
        rep_action = self.env["report"].get_action(self, rep_name)
        rep_action['data'] = custom_data
        return rep_action


class ExpenseLine(models.TransientModel):
    _name = 'expense.line'

    name = fields.Char('Concept')
    sales = fields.Float('Sales')
    cost = fields.Float('Costs')
    margin = fields.Float('Margin')
    cost_per = fields.Float('% Costs')
    margin_per = fields.Float('% Margin')
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
        """
        Return a dict to create a expense line that represents a row of the
        computed table.
        """
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
                                    'total_sale', 'total_general']:
                if e.compute_type == 'total_cost':
                    v['cost'] = self._totalizator(values, 'cost')
                    v['cost_per'] = (v['cost'] / (sales or 1.0)) * 100
                elif e.compute_type == 'total_margin':
                    v['margin'] = last_margin
                    v['margin_per'] = (v['margin'] / (sales or 1.0)) * 100
                elif e.compute_type == 'total_sale':
                    v['sales'] = self._totalizator(values, 'sales')
                elif e.compute_type == 'total_general': # All totalizators in one
                    v['cost'] = self._totalizator(values, 'cost')
                    v['cost_per'] = (v['cost'] / (sales or 1.0)) * 100
                    v['margin'] = last_margin
                    v['margin_per'] = (v['margin'] / (sales or 1.0)) * 100
                    v['sales'] = self._totalizator(values, 'sales')
                res[e.id] = v
                values.append(v)
                continue

            # Compute columns
            if e.compute_type == 'invoicing':
                col_type = 'sales'
            elif e.compute_type == 'analytic':
                col_type = e.expense_type_id.col_type
            else:
                col_type = 'cost'

            if col_type == 'sales':
                if first:  # First time
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
        return values

    def _get_var_ratio(self, partner, e, compute_type):
        """
        Returns the fixed ratio if selected in the element type, or compute
        the total facturation and get the ration between partner facturation
        and total facturation
        """
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
            # Invoiced - Returned
            t1 = q1 - q2

            query = self._get_invoice_query(e, partner, 'out_invoice')
            self._cr.execute(query)
            qres = self._cr.fetchall()
            q1 = qres[0][0] if qres[0][0] is not None else 0.0

            query = self._get_invoice_query(e, partner, 'out_refund')
            self._cr.execute(query)
            qres = self._cr.fetchall()
            q2 = qres[0][0] if qres[0][0] is not None else 0.0
            # Invoiced - Returned
            t2 = q1 - q2
            # The computed ratio
            res = t2 / t1
        return res

    def _analytic_compute_amount(self, e, partner):
        """
        Get the amount based on analytic account of a analytic journal if
        a journal is selected in the element type
        """
        res = 0.0
        query = self._get_analytic_query(e, partner)
        if not query:
            return res
        self._cr.execute(query)
        qres = self._cr.fetchall()
        res = qres[0][0] * (-1) if qres[0][0] is not None else 0.0
        return res

    def _invoicing_compute_amount(self, e, partner):
        """
        Gets the invoiced amount based on the open and draft invoices
        """
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

    def _get_analytic_query(self, e, partner):
        
        def get_analytic_recursive(analytic_ids):
            res = []
            analytic_obj = self.env['account.analytic.account']
            if not analytic_ids:
                return res
            aac_ids = []
            for analytic_id in analytic_ids:
                new_aac_ids = [analytic_id.id]
                while new_aac_ids:
                    aac_ids += new_aac_ids
                    analytic_ids_to_browse = new_aac_ids
                    new_aac_ids = []
                    for account in analytic_obj.browse(analytic_ids_to_browse):
                        new_aac_ids += map(lambda x: x.id,
                                    [child for child in account.child_ids
                                     if child.state != 'template'])
            res = list(set(aac_ids))
            return res

        aac = []
        if partner:
            for partner_id in partner:
                aad = self.env['account.analytic.default'].\
                    search([('partner_id', '=', partner_id.id)], limit=1)
                if not aad:
                    return False
                aac += aad.analytic_id
        aac = list(set(aac))
        aac_ids = get_analytic_recursive(aac)
        exp_type = e.expense_type_id
        journal_id = exp_type.journal_id.id if exp_type.journal_id else False

        if partner and exp_type.restrict_partner:
            query = """
                SELECT sum(aal.amount) 
                FROM account_analytic_line aal
                INNER JOIN account_move_line aml ON aal.move_id = aml.id
                INNER JOIN res_partner rp ON aml.partner_id = rp.id
                WHERE aal.date >= '%s' AND aal.date <= '%s'
                  AND aal.company_id = %s
            """ % (self._context['from_date'], self._context['to_date'], 
                   e.structure_id.company_id.id)
            if len(partner) == 1:
                query += """ AND rp.commercial_partner_id = %s """ % str(partner[0].id)
            else:
                query += """ AND rp.commercial_partner_id in %s """ % str(tuple([x.id for x in partner]))
        else:
            query = """
                SELECT sum(aal.amount)
                FROM account_analytic_line aal
                WHERE aal.date >= '%s' AND aal.date <= '%s'
                  AND aal.company_id = %s
            """ % (self._context['from_date'], self._context['to_date'], 
                   e.structure_id.company_id.id)
        if partner:
            if len(aac_ids) == 1:
                query += """ AND aal.account_id = %s """ % str(aac_ids[0])
            else:
                query += """ AND aal.account_id in %s """ % str(tuple(aac_ids))
        if journal_id:
            query += """ AND aal.journal_id = %s """ % str(exp_type.journal_id.id)
        if exp_type.product_id:
            query += """ AND aal.product_id = %s """ % exp_type.product_id.id
        elif exp_type.categ_id:
            domain = [('categ_id', 'child_of', exp_type.categ_id.id)]
            prod_objs = self.env['product.product'].search(domain)
            product_ids = [p.id for p in prod_objs]
            if product_ids:
                if len(product_ids) == 1:
                    query += """ AND aal.product_id = %s """ % product_ids[0]
                else:
                    query += """ AND aal.product_id in
                    %s """ % str(tuple(product_ids))
        return query

    def _get_invoice_query(self, e, partner, inv_type):
        """
        Return query to get the invoiced between periods for a partner and
        optionale by product and categories.
        """
        exp_type = e.expense_type_id
        query = """
            SELECT sum(price_subtotal)
            FROM account_invoice_line ail
            INNER JOIN account_invoice ai ON ai.id = ail.invoice_id
            WHERE ai.date_invoice >= '%s' AND
                  ai.date_invoice <= '%s' AND ai.company_id = %s AND
                  ai.state in ('open', 'paid') AND
                  type = '%s'
        """ % (self._context['from_date'], self._context['to_date'], 
               e.structure_id.company_id.id, inv_type)
        if partner:
            if len(partner) == 1:
                query += """ AND ai.commercial_partner_id = %s """ % str(partner[0].id)
            else:
                query += """ AND ai.commercial_partner_id in %s """ % str(tuple([x.id for x in partner]))
        if exp_type.product_id:
            query += """ AND ail.product_id = %s """ % exp_type.product_id.id
        elif exp_type.categ_id:
            domain = [('categ_id', 'child_of', exp_type.categ_id.id)]
            prod_objs = self.env['product.product'].search(domain)
            product_ids = [p.id for p in prod_objs]
            if product_ids:
                if len(product_ids) == 1:
                    query += """ AND ail.product_id = %s """ \
                    % product_ids[0]
                else:
                    query += """ AND ail.product_id in %s """ \
                    % str(tuple(product_ids))
        return query

    def _totalizator(self, values, key):
        total = 0.0
        for v in values:
            if v['compute_type'] in ['total_cost', 'total_margin',
                                     'total_sale', 'total_general']:
                continue
            total += v[key]
        return total

    @api.model
    def _create_expense_lines(self, line_values):
        res = []
        for v in line_values:
            vals = {
                'name': v['name'],
                'compute_type': v['compute_type'],
                'sales': round(v['sales'], 2),
                'cost': round(v['cost'], 2),
                'margin': round(v['margin'], 2),
                'cost_per': round(v['cost_per'], 2),
                'margin_per': round(v['margin_per'], 2),
            }
            expense_line = self.create(vals)
            res.append(expense_line.id)
        return res
