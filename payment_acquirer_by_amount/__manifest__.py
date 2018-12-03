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
    'name': 'Payment Acquirer By Amount',
    'version': '1.0',
    'summary': 'Set amounts to show payment acquirer in your website by these ones amounts',
    'description': 'You can establish a minimun amount, a maximun amount or both to show payment acquirer in your \
        website by these ones amounts',
    'category': 'Accounting',
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'license': 'AGPL-3',
    'contributors': [
        "Comunitea ",
        "Ruben Seijas <ruben@comunitea.com>"
    ],
    'depends': ['payment'],
    'data': [
        'views/payment_view.xml',
        'views/payment_templates.xml'
    ],
    'images': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
