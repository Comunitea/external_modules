##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2023 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
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
    "name": "Delivery DHL EXpress",
    "summary": "Delivery Carrier implementation for DHL Express",
    "version": "16.0.1.0.0",
    "category": "Stock",
    "website": "www.comunitea.com",
    "author": "Comunitea",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "delivery",
        "delivery_state",
        "sale_shipping_info_helper",
        "stock_picking_report_valued",
        "product_harmonized_system",
    ],
    "data": [
        "views/delivery_dhl_express_view.xml",
        "views/product_template_view.xml",
        "views/stock_picking.xml",
        "data/cron.xml",
        "data/parameters.xml",
        "views/res_partner.xml",
    ],
}
