# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2019 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'warehouse_apk',
    'version': '12.0.0.0',
    'summary': 'Customizations needed by the warehouse apk',
    'category': 'Custom',
    'author': 'comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'sale_stock',
        'stock_move_location',
        'stock_picking_type_group'
    ],
    'data': [
        'views/stock_move.xml',
        'views/stock_picking.xml',
        'views/stock_warehouse.xml',
        'views/product.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
