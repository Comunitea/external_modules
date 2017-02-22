## -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2013 QUIVAL, S.A. All Rights Reserved
#    $Pedro Gómez Campos$ <pegomez@elnogal.com>
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
    'name': 'Intrastat reports for Spain Localization',
    'version': '1.0',
    'description': """
    This module contains the localization part for intrastat reporting for Spain and extends the intrastat_base module.
    """,
    'category': 'Localisation/Report Intrastat',
    'author': 'Pedro Gómez',
    'website': 'www.elnogal.com',
    'depends': [
        "stock",
        "l10n_es_aeat_mod349",
        "intrastat_base",
        "intrastat_product",
        "picking_invoice_rel",
    ],
    'init': [],
    'update_xml': [
        'security/intrastat_security.xml',
        'security/ir.model.access.csv',
        'intrastat_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': False,
}
