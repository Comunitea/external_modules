# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Early payment discount',
    'summary': """ Adds early payment discount
                    """,
    'version': '12.0.1.0.0',
    'author': 'Pexego',
    'maintainer': 'Comunitea',
    'license': 'AGPL-3',
    'depends': ['base', 'product', 'account',],
    'category': 'Enterprise Specific Modules',
    'data': ['security/ir.model.access.csv',
              'security/security.xml',
              'data/product_product.xml',
              'views/partner_payment_term_early_discount_view.xml',
              'views/partner_view.xml',
              'views/payment_term_view.xml',
              'views/account_invoice_view.xml',
              'views/product_category_view.xml'],
    'installable': True
}
