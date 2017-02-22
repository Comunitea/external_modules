# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos All Rights Reserved
#    $Marta Vázquez Rodríguez$ <marta@pexego.es>
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
        "name" : "Purchases forecast",
        "version" : "1.0",
        "author" : "Pexego",
        "website" : "http://www.pexego.es",
        "category" : "Purchases",
        "description": """Purchases forecast""",
        "depends" : ['purchase','base'],
        "init_xml" : [],
        "demo_xml" : [],
        "data" : [ 'data/purchases_forecast_line_seq.xml',
                         'security/purchases_forecast_security.xml',
                         'purchases_forecast_view.xml',
                         'purchases_forecast_workflow.xml',
                         'wizard/merge_purchase_forecast_view.xml',
                         'security/ir.model.access.csv'
            ],
        "installable": False,

}
