# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Delivery Packing List',
    'version': '11.0.0.0.0',
    'category': 'Custom',
    'license': 'AGPL-3',
    'author': "Comunitea, ",
    'depends': [
        'delivery',
    ],
    'data': [
        'views/stock_picking.xml',
        'security/ir.model.access.csv',
        'report/delivery_packing_report.xml'
    ],
    'installable': True,
}
