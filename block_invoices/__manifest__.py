# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    @author Alberto Luengo Cabanillas
#    Copyright (C) 2016
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
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
    'name': "Block Invoices",
    'version': '8.0.1.0.0',
    'category': 'Accounting',
    'description': """Block sales and invoices for customers from due dates.""",
    'author': 'Alberto Luengo, Comunitea',
    'website': 'luengocabanillas.com, http://www.comunitea.com',
    "depends": ['sale','stock_account'],
    "data": ['res_company_view.xml','res_partner_view.xml', 'sale_view.xml', 'account_invoice_view.xml', 'data/ir_cron.xml'],
    "installable": False
}
