# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 NaN Projectes de Programari Lliure, S.L.
#                       http://www.NaN-tic.com
#    Copyright (C) 2013 Pexego Sistemas Informáticos S.L.
#                       http://www.pexego.es
#    Copyright (C) 2016 Comunitea Servicios Tecnológicos S.L.
#                       http://www.comunitea.com
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
    'name': 'Partner Paydays',
    'version': '10.0.0.0.0',
    'description': """"This module adds fields to introduce partner's paydays
& holidays. It also allows due date in customer invoices to take into account
vacations if the partner doesn't pay during that period.""",
    "author": "Nan,Pexego \n contributor readylan, Comunitea",
    'website': 'http://www.NaN-tic.com, http://www.comunitea.com',
    'depends': ['account'],
    'category': 'Custom Modules',
    'data': [
        'views/partner_paydays_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
