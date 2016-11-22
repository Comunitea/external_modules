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
