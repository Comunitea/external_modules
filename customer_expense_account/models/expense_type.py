# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields

COMPUTE_TYPES = [
    ('analytic', 'Based on partner analytic account'),
    ('ratio', 'Based on parent element'),
    ('total_cost', 'Totalizator cost'),
    ('total_margin', 'Totalizator margin'),
    ('distribution', 'Distribution over analytic account'),
]

RATIO_COMPUTE_TYPES = [
    ('fixed', 'Fixed'),
    ('invoices', 'Compute over invoices'),
    ('kgs', 'Compute over Kg'),
    ('units', 'Compute over Units'),
    ('hours', 'Compute over hours'),
]


class ExpenseType(models.Model):
    _name = 'expense.type'

    name = fields.Char('Expense Type', required=True)
    compute_type = fields.Selection(COMPUTE_TYPES, 'Compute Type',
                                    required=True,
                                    default='analytic')
    journal_id = fields.Many2one('account.analytic.journal',
                                 'Analytic Journal')
    ratio = fields.Float('Ratio')
    analytic_id = fields.Many2one('account.analytic.account',
                                  'Analytic Account')
    ratio_compute_type = fields.Selection(RATIO_COMPUTE_TYPES,
                                          string='Ratio Compute Type',
                                          default='fixed')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self:
                                 self.env['res.company'].
                                 _company_default_get('expense.type'))
