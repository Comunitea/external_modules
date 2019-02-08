# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock APK Version 12',
    'summary': 'Add functions for stock apk',
    'version': '11.0.1.0.0',
    'category': 'warehouse',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'stock',


    ],
    'data': [
        'views/stock_picking.xml',
        'views/stock_move.xml',
        'views/stock_quant_package.xml',
        'views/stock_location.xml',
        'views/product_template.xml'
    ],
}