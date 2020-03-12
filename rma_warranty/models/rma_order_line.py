# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class RmaOrderLine(models.Model):

    _inherit = "rma.order.line"

    @api.onchange("lot_id")
    def onchange_lot_id_warranty(self):
        if self.lot_id:
            if (
                self.lot_id.warranty_termination
                and self.lot_id.warranty_termination > fields.Date.today()
            ):
                self.under_warranty = True
            else:
                self.under_warranty = False
