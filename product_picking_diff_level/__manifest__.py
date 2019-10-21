# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Product Picking Cost',
    'version': '11.0.0.0.0',
    'category': 'Custom',
    'license': 'AGPL-3',
    'author': "Comunitea, ",
    'depends': [
        'sale_stock', 'stock_batch_picking'
    ],
    'data': [
        'views/stock_move.xml',
        'views/product_template.xml',
        'views/stock_location.xml',
        'views/stock_batch_picking.xml',
        'views/stock_picking.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
}

