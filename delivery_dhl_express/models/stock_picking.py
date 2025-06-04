##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2022 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
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
import time
from datetime import datetime, timedelta
from odoo import _, models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    request_date = fields.Char("Requested Date")
    dhl_express_shipment_reference = fields.Char('DHL Express Shipment Reference')
    dhl_express_confirmation_number = fields.Char('DHL Express Dispatch Confirmation Number')

    def compute_request_date(self):
        for picking in self:
            calculated_picking_time = "{:%H:%M:%S}".format(
                datetime.now() + timedelta(hours=1)
            )
            picking_time = time.strftime(
                "%Y-%m-%dT{}%Z".format(calculated_picking_time), time.gmtime()
            )
            k = "{}:{}".format(
                time.strftime("%z", time.gmtime())[:3],
                time.strftime("%z", time.gmtime())[3:],
            )
            picking.request_date = "{}{}".format(picking_time, k)
