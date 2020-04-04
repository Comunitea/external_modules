# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class StockProductionLot(models.Model):

    _inherit = "stock.production.lot"

    warranty_termination = fields.Date()
