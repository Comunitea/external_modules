# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class RmaOrderLine(models.Model):

    _inherit = 'rma.order.line'

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.partner_id not in res.message_partner_ids:
            res.message_subscribe([res.partner_id.id])
        return res


