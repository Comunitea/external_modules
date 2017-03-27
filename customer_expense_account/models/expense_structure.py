# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.tools.translate import _
from expense_type import COMPUTE_TYPES
from expense_type import RATIO_COMPUTE_TYPES


class ExpenseStructure(models.Model):
    _name = 'expense.structure'

    name = fields.Char('Name', required=True)
    element_ids = fields.One2many('expense.structure.elements', 'structure_id',
                                  string="Elements", copy=True)
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self:
                                 self.env['res.company'].
                                 _company_default_get('expense.structure'))

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = _('%s (copy)') % self.name
        res = super(ExpenseStructure, self).copy(default)
        # Elements based on parent elements, must be mapped to new copied ids
        old_new_ids = dict(zip([x.id for x in self.element_ids],
                               [x.id for x in res.element_ids]))
        for element_id in res.element_ids.filtered(lambda r: r.parent_id):
            element_id.parent_id = old_new_ids[element_id.parent_id.id]
        return res


class ExpenseStructureElements(models.Model):
    _name = 'expense.structure.elements'
    _rec_name = 'expense_type_id'
    _order = 'sequence'

    name = fields.Char('Name')
    structure_id = fields.Many2one('expense.structure', 'Structure',
                                   ondelete="cascade")
    sequence = fields.Integer('Sequence', require=True)
    expense_type_id = fields.Many2one('expense.type', 'Expense Type',
                                      required=True)
    compute_type = fields.Selection(COMPUTE_TYPES, 'Compute Type',
                                    readonly=True,
                                    related='expense_type_id.compute_type')
    ratio = fields.Float('Ratio')
    var_ratio = fields.Float('Ratio')
    parent_id = fields.Many2one('expense.structure.elements', 'Parent Element')
    ratio_compute_type = \
        fields.Selection(RATIO_COMPUTE_TYPES, 'Compute Type',
                         readonly=True,
                         related='expense_type_id.ratio_compute_type')

    @api.onchange('expense_type_id')
    def onchange_expense_type_id(self):
        """
        Gets by default same name as expense type associed.
        """
        self.name = self.expense_type_id.name
