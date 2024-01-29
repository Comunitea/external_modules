##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2022 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See thefire
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Login Digital Kit',
    'version': '15.0.1.0.0',
    'category': 'Custom',
    'author': 'Comunitea,',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'web',
    ],
    'data': [
        'templates/webclient_templates.xml',
        'views/res_company.xml',
    ],
    "assets": {
        "web.assets_backend": [
            'login_digital_kit/static/src/js/backendlogo.js',
            'login_digital_kit/static/src/xml/backendlogo.xml',
        ],
    },
}
