# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields

COMPUTE_TYPES = [
    ('analytic', 'Based on analytic account'),
    ('ratio', 'Based on parent element'),
    ('total_cost', 'Total Cost'),
    ('total_margin', 'Total Margin'),
    ('distribution', 'Based on analytic distribution'),
]


class ExpenseType(models.Model):
    _name = 'expense.type'

    name = fields.Char('Expense Type', required=True)
    compute_type = fields.Selection(COMPUTE_TYPES, 'Compute Type',
                                    required=True,
                                    default='analytic')
    journal_id = fields.Many2one('account.analytic.journal', 'Journal')
    ratio = fields.Float('Ratio')
