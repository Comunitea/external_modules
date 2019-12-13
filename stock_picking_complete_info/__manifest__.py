# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Stock Picking Complete Info',
    'version': '12.0.0.0.0',
    'category': 'Custom',
    'license': 'AGPL-3',
    'author': "Comunitea, ",
    'depends': [
        'sale_stock',
        'stock_picking_batch_extended',
        'web_tree_dynamic_colored_field'
    ],
    'data': [
        'views/stock_picking.xml',
        'views/stock_batch_picking.xml',
    ],
    'installable': True,
}


