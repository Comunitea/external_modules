# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields

COMPUTE_TYPES = [
    ('analytic', 'Based on partner account'),
    ('ratio', 'Based on parent element'),
    ('total_cost', 'Totalizator Cost'),
    ('total_margin', 'Totalizator Margin'),
    ('distribution', 'Distribution over analytic account'),
]

RATIO_COMPUTE_TYPES = [
    ('fixed', 'Defined by user'),
    ('invoices', 'Over Invoices'),
]


class ExpenseType(models.Model):
    _name = 'expense.type'

    name = fields.Char('Expense Type', required=True)
    compute_type = fields.Selection(COMPUTE_TYPES, 'Compute Type',
                                    required=True,
                                    default='analytic')
    journal_id = fields.Many2one('account.analytic.journal', 'Journal')
    ratio = fields.Float('Ratio')
    analytic_id = fields.Many2one('account.analytic.account',
                                  'Analytic Account')
    ratio_compute_type = fields.Selection(RATIO_COMPUTE_TYPES, 'Compute Type',
                                          default='fixed')
