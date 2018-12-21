# -*- coding: utf-8 -*-
#
# © 2018 Comunitea
# Ruben Seijas <ruben@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#
##############################################################################
#
#    Copyright (C) {year} {company} All Rights Reserved
#    ${developer} <{mail}>$
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
    'name': 'Paga+Tarde Payment Acquirer',
    'version': '1.0',
    'summary': 'Añade el método de pago: Paga+Tarde',
    'description': '',
    'category': 'Accounting',
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'license': 'AGPL-3',
    'contributors': [
        "Ruben Seijas <ruben@comunitea.com>"
    ],
    'depends': [
        'payment',
        'website_sale',  # For default checkout
        # 'website_sale_one_step_checkout'  # For OSC checkout
    ],
    'data': [
        'views/payment_views.xml',
        'views/payment_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}