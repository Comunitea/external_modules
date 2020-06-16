# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Early payment discount',
    'description' : """ Adds early payment discount
                    """,
    'version' : '10.0.1.0.0',
    'author' : 'Pexego',
    'depends' : ['base', 'product', 'account', 'sale', 'sale_stock', 'stock',
                 'stock_account', 'decimal_precision',
                 'account_analytic_default'],
    'category' : 'Enterprise Specific Modules',
    'data' : ['security/ir.model.access.csv',
              'security/security.xml',
              'data/product_product.xml',
              'views/partner_payment_term_early_discount_view.xml',
              'views/partner_view.xml',
              'views/payment_term_view.xml',
              'views/sale_view.xml',
              'views/account_invoice_view.xml',
              'views/product_category_view.xml',
              'report/sale_order.xml'],
    'installable': True
}
