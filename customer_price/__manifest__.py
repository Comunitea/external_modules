# © 2019 Comunitea - Santi Argüeso <santi@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Precios de venta por cliente',
    'summary': 'Establecer precios específicos de venta por cliente',
    'version': '12.0.1.0.0',
    'category': 'partner',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'product',
    ],
    'data': [
        'views/customer_price.xml',
        'views/product_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
        'security/customer_price_security.xml'
    ],
}