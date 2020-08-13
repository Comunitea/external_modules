# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Early payment discount for sales',
    'summary' : """Adds early payment discount for sales""",
    'version' : '12.0.1.0.0',
    'author' : 'Comunitea',
    'maintainer' : 'Comunitea',
    'depends' : ['sale_stock', 'account'],
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
