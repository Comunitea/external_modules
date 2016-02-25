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
        "name" : "Account bank transfers",
        "description": "Allow to execute transfers between journal using wizard",
        "version" : "8.0.1.0.0",
        "author" : "Comunitea",
        "website" : "http://www.comunitea.com",
        "category" : "Accounting",
        "depends" : ['account'],
        "init_xml" : [],
        "demo_xml" : [],
        "data" : ['wizard/bank_transfer_wizard_view.xml'],
        "installable": True,
        'active': False

}
