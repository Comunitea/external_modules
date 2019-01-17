# -*- coding: utf-8 -*-
#
# © 2016 Comunitea
# © 2019 Comunitea Ruben Seijas <ruben@comunitea.com>
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
    'name': 'Website Sale Filter Countries',
    'summary': 'Create a new field website_available to publish countries and country states in website',
    'version': '10.0',
    'category': 'E-Commerce: External',
    'website': 'http://www.comunitea.com',
    'author': 'Comunitea',
    'contributors': [
        "Ruben Seijas <ruben@comunitea.com>"
    ],
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'website_sale',
        'website_portal',
        # 'website_snippet_country_dropdown'  # To use this it is necessary install sass
    ],
    'data': [
        'views/res_country.xml',
        'views/snippet.xml'
    ],
}
