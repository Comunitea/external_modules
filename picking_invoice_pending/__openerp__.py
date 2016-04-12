# -*- coding: utf-8 -*-
##############################################################################
#
#    Authors: Santiago Argüeso
#    Copyright Comunitea SL 2015
#    Omar Castiñeira Saavedra Copyright Comunitea SL 2015
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
    'name': 'Pending invoices accounting from  Picking',
    'description': "Allow to account invoices when transfering incoming "
                   "pickings. "
                   "When invoice is validated previous account move "
                   "is reverted.",
    'version': '1.1',
    'author': 'Comunitea',
    'category': 'Finance',
    'website': 'http://comunitea.com',
    'depends': ['base',
                'account',
                'account_reversal',
                'stock',
                'purchase_discount',
                'picking_invoice_rel'],
    'data': ['res_company_view.xml',
             'stock_picking_view.xml'],
    'active': False,
    'installable': True,
}
