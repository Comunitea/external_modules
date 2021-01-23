##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2020 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
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

from odoo import api, fields, models

class CarrierAccount(models.Model):
    _inherit = "carrier.account"

    integration_type = fields.Selection(selection_add=[("ncx", "NACEX")])
    ncx_client = fields.Char("NACEX Client Code")
    ncx_delegation = fields.Char("NACEX Delegation Code")
    ncx_client_department = fields.Char("NACEX Franchise Code")
    ncx_printer_model = fields.Selection(
        [
            ("TECSV4_B", "TECSV4_B"),
            ("TECEV4_B", "TECEV4_B"),
            ("TECFV4_B", "TECFV4_B"),
            ("ZEBRA_B", "ZEBRA_B"),
            ("IMAGEN_B", "IMAGEN_B"),
        ],
        default="TECSV4_B",
    )
    ncx_payment_type = fields.Selection(
        [
            ("O", "Payment on origin"),
            ("D", "Payment on destination"),
            ("T", "Payment by a third party"),
        ],
        default="O",
    )
    ncx_package_type = fields.Selection(
        [
            ("0", "Documents"),
            ("1", "Nacex Bag"),
            ("2", "Nacex Cardboard Box"),
        ],
        default="2",
    )
    ncx_pod_type = fields.Selection(
        [
            ("N", "No"),
            ("O", "Origin"),
            ("D", "Destination"),
            ("A", "Payment on pick up"),
        ],
        default="D",
    )