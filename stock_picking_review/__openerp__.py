# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
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
    'name': 'Stock Picking review picking',
    'version': '1.0',
    'category': 'stock',
    'description': """""",
    'author': 'COMUNITEA',
    'website': '',
    "depends": ['stock_valued_picking',
                'web_action_conditionable',
                'stock_picking_invoice_link'],
    "data": [
        'stock_picking_view.xml',
        'stock_data.xml',
        'wizard/fast_return.xml'],

    "installable": True
}
