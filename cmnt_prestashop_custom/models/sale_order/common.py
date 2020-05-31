# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrde(models.Model):

    _inherit = "sale.order"

    prestashop_state = fields.Many2one("sale.order.state")

    def write(self, vals):
        res = super().write(vals)
        for order in self:
            if vals.get("prestashop_state"):
                state = order.prestashop_state
                if state.trigger_cancel:
                    order.invoice_ids.filtered(
                        lambda r: r.state == "draft"
                    ).action_cancel()
                    if order.state == "done":
                        order.action_unlock()
                    order.action_cancel()
        return res
