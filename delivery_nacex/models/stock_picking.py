##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
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
from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipment_reference = fields.Char("Shipment Reference")
    delivery_note = fields.Char(compute="_compute_delivery_note")
    ncx_payment_on_delivery = fields.Boolean("POD", default=False)
    ncx_pdo_quantity = fields.Monetary(
        string='Total',
    )

    def nacex_get_label(self):
        self.ensure_one()
        tracking_ref = self.carrier_tracking_ref
        if self.delivery_type != "nacex" or not tracking_ref:
            return
        self.carrier_id.nacex_save_label(self)

    @api.depends("sale_id")
    def _compute_delivery_note(self):
        for pick in self:
            delivery_note = ""
            if pick and pick.sale_id:
                delivery_note += "{} ".format(pick.sale_id.note)
            if delivery_note.strip() == "":
                delivery_note = "N/A"
            pick.delivery_note = delivery_note[:45]
