# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# © 2017 El Nogal  - Pedro Gómez <pegomez@elnogal.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields

COMPUTE_TYPES = [
    ('analytic', 'Based on partner analytic account'),
    ('invoicing', 'Based on invoicing'),
    ('ratio', 'Based on parent element'),
    ('total_cost', 'Totalizator cost'),
    ('total_margin', 'Totalizator margin'),
    ('total_sale', 'Totalizator sales'),
    ('total_general', 'Totalizator general'),
    ('distribution', 'Distribution over analytic account'),
]

RATIO_COMPUTE_TYPES = [
    ('fixed', 'Fixed'),
    ('invoicing', 'Compute over invoices'),
]

COLUMN_TYPES = [
    ('sales', 'Sales'),
    ('cost', 'Cost'),
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
    product_id = fields.Many2one('product.product', 'Product')
    categ_id = fields.Many2one('product.category', 'Product Category')
    restrict_partner = fields.Boolean('Only analytic moves of customer', 
            help='If check, only the analytic moves in which the customer '
            'of the related account move matches the selected customer '
            'will be considered.')
    col_type = fields.Selection(COLUMN_TYPES,
                                string='Column',
                                default='cost')
