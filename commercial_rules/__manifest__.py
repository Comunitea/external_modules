# -*- coding: utf-8 -*-
# © Openlabs Technologies & Consulting (P) Limited
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Commercial Rules',
    'version': '10.0.0.0.1',
    'author': 'Openlabs Technologies & Consulting (P) Limited, ',
              'Comunitea'
    'website': 'http://openlabs.co.in', 'http://www.comunitea.com'
    'category': 'Generic Modules/Sales & Purchases',
    'depends': ['base', 'sale_stock'],
    'data': [
        'data/product_data.xml',
        'views/rule_view.xml',
        'views/sale.xml',
        'views/res_partner_view.xml',
        'views/product_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
