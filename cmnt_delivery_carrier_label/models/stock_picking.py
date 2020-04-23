# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_generate_carrier_label(self):
        raise NotImplementedError(
            _("No label is configured for the selected delivery method.")
        )

    carrier_weight = fields.Float()
    carrier_packages = fields.Integer(default=1)
    carrier_service = fields.Many2one('delivery.carrier.service')
