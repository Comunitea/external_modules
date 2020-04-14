##############################################################################
#
#    Copyright (C) 2015 Comunitea Servicios Tecnológicos All Rights Reserved
#    $Omar Castiñeira Saaevdra <omar@comunitea.com>$
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
    'name': 'Rappel management',
    'author': 'Comunitea',
    'category': 'Sale',
    'version': '12.0.1.0.0',
    'website': 'www.comunitea.com',
    'description': """
Rappel Management
=====================================================

    """,
    'depends': ['account',
                'sale_stock',
                'product'],
    'data': ['views/rappel_type_view.xml',
             'views/rappel_view.xml',
             'views/rappel_info_view.xml',
             'views/res_partner_view.xml',
             'views/rappel_menus.xml',
             'data/rappel_mail_advice_data.xml',
             'data/ir.cron.xml',
             'wizard/compute_rappel_invoice_view.xml',
             'security/ir.model.access.csv',
             'views/sale_view.xml',
             'views/account_invoice_view.xml'],
    'installable': True,
    'application': False,
}
