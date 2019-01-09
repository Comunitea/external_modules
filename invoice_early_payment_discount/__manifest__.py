# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Invoice Early payment discount',
    'summary': """ Adds early payment discount on invoices
                    """,
    'version': '11.0.1.0.0',
    'author': 'Comunitea',
    'maintainer': 'Comunitea',
    'license': 'AGPL-3',
    'depends': ['base', 'product', 'account', 
                'account_analytic_default'],
    'category': 'Custom',
    'data': [ 'security/ir.model.access.csv',
              'security/security.xml',
              'data/product_product.xml',
              'views/partner_payment_term_early_discount_view.xml',
              'views/partner_view.xml',
              'views/payment_term_view.xml',
              'views/account_invoice_view.xml',
              'views/product_category_view.xml',
            ],
    'installable': True
}
