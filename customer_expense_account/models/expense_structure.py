# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ExpenseStructure(models.Model):
    _name = 'expense.structure'

    name = fields.Char('Name', required=True)
    element_ids = fields.One2many('expense.structure.elements', 'structure_id',
                                  string="Elements")
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self:
                                 self.env['res.company'].
                                 _company_default_get('expense.structure'))


class ExpenseStructureElements(models.Model):
    _name = 'expense.structure.elements'
    _rec_name = 'expense_type_id'

    expense_type_id = fields.Many2one('expense.type', 'Expense Type')
    structure_id = fields.Many2one('expense.structure', 'Structure',
                                   required=True)
    sequence = fields.Integer('Sequence', require=True)


class ExpenseLine(models.TransientModel):
    _name = 'expense.line'

    name = fields.Char('Concept')
    sales = fields.Float('Sales')
    cost = fields.Float('Costs')
    margin = fields.Float('Margin')
    cost_per = fields.Float('% Costs')
    margin_per = fields.Float('% Margin')

    @api.model
    def show_expense_lines(self):
        line_ids = []
        print "ACTIVE ID"
        print self._context.get('active_id')
        for a in [1, 2, 3, 4, 5]:
            vals = {
                'name': str(a),
                'sales': a,
                'costs': a,
                'margin': a,
                'cost_per': a,
                'margin_per': a,
            }
            expense_line = self.create(vals)
            line_ids.append(expense_line.id)
        res = {
            'domain': str([('id', 'in', line_ids)]),
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'expense.line',
            'type': 'ir.actions.act_window',
            'nodestroy': True
        }
        return res
