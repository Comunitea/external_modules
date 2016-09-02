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
    "name": "Product Cost Management",
    "description": """
       Product Cost Management.
        """,
    "version": "1.0",
    "author": "Pexego",
    "depends": ["base",
                "stock",
                "product",
                "account",
                "stock_account",
                "mrp"],
    "category": "Product",
    "init_xml": [],
    "data": ["wizard/product_costs_view.xml",
             "wizard/stock_valuation_history_view.xml",
              "views/cost_type_view.xml",
              "views/cost_structure_elements.xml",
              "data/product_cost_management_names_seq.xml",
              "data/ir_cron.xml",
              "views/product.xml",
              "views/product_cost_management_menus.xml",
              "security/ir.model.access.csv",
              "security/product_cost_security.xml",
             ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
