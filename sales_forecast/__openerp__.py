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
        "name" : "Sales forecast",
        "version" : "1.0",
        "author" : "Pexego",
        "website" : "http://www.pexego.es",
        "category" : "Sales",
        "description": """Sales forecast""",
        "depends" : ['product','stock','account','base'],
        "init_xml" : [],
        "demo_xml" : [],
        "data" : ["data/sales_forecast_line_seq.xml",
                        "security/sales_forecast_security.xml",
                        "sales_forecast_workflow.xml",
                        "sales_forecast_view.xml",
                        "wizard/get_sales_forecast_view.xml",
                        "security/ir.model.access.csv",
                        "wizard/merge_sales_forecast_view.xml",
                        "wizard/scale_sales_forecast_view.xml"
            ],
        "installable": True,
        'active': False

}
