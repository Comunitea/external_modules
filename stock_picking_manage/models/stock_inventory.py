# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class StockInventoryLine(models.Model):

    _inherit = "stock.inventory.line"

    def _get_quants(self):
        return super()._get_quants()

