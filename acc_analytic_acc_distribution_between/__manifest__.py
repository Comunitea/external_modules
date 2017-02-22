# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
#    $Omar Castiñeira Saavedra$
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
    'name': 'Analytic accounting and analytic distribution accounting together',
    'version': '8.0.1.0.0',
    'category': 'Accounting',
    'description': """
        Allow to use analytic distributions and analytic accounts together
        """,
    'author': 'Comunitea',
    'website': 'https://www.comunitea.com',
    'depends': ['base', 'account', 'analytic', 'account_analytic_plans',
                'account_analytic_default'],
    'init_xml': [],
    'data': ['account_view.xml'],
    'demo_xml': [],
    'installable': False,
    'certificate': '',
}
