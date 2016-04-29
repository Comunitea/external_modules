# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Comunitea Servicios Tecnológicos All Rights Reserved
#    $Carlos Lombardía <carlos@comunitea.com>$
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
    'name': "Harmonized System Codes",
    'version': '1.0',
    'category': 'stock',
    'description': """HS Codes""",
    'author': 'Comunitea',
    'website': 'www.comunitea.com',
    "depends": ['base', 'product', 'purchase', 'account', 'stock',
                'report_intrastat'],
    "data": ['hs_codes_view.xml',
             'security/ir.model.access.csv'],
    "installable": True
}
