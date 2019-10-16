# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Stock Picking Custom Anzamar',
    'version': '11.0.0.0.0',
    'category': 'Custom',
    'license': 'AGPL-3',
    'author': "Comunitea, ",
    'depends': [
        'stock_batch_picking',
    ],
    'data': [
        'data/res_partner_category.xml',
        'data/stock_location_cron.xml',
        'views/stock_batch_picking.xml',
        'views/stock_location.xml',
        'views/stock_move.xml',
        'views/stock_picking.xml',
        'report/stock_picking_delivery_tag.xml',
        'report/report_stock_picking_view.xml',
        'wizard/stock_import.xml'
    ],
    'installable': True,
}
