# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Stock Move Reassign Availability',
    'version': '11.0.0.0.0',
    'category': 'Custom',
    'license': 'AGPL-3',
    'author': "Comunitea, ",
    'depends': [
        'stock'
    ],
    'data': [
        #'data/data.xml',
        'security/ir.model.access.csv',
        'views/stock_move.xml',
        'wizard/stock_move_change_reserve_wzd.xml'
    ],
    'installable': True,
}


