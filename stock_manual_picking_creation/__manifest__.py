# -*- coding: utf-8 -*-
# © 2018 Comunitea -Javier Colmenero <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Manual Picking Creation',
    'summary': 'Avoid assign picking to moves in order confirm',
    'version': '11.0.1.0.0',
    'category': 'warehouse',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale_stock',
        'stock_picking_imp',  # patch to separate domain from action_assign
    ],
    'data': [
        'views/sale_view.xml',
        'views/stock_move.xml',
        # 'views/stock_picking.xml',
    ],
}