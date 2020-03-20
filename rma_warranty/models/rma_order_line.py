# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class RmaOrderLine(models.Model):

    _inherit = "rma.order.line"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.calculate_under_warranty()
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if "lot_id" in vals:
            for rma in self:
                rma.calculate_under_warranty()
        return res

    def calculate_under_warranty(self):
        if self.lot_id:
            if (
                self.lot_id.warranty_termination
                and self.lot_id.warranty_termination > fields.Date.today()
            ):
                self.under_warranty = True
            else:
                self.under_warranty = False
