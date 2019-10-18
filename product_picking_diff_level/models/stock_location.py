# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class StockLocation(models.Model):
    _inherit = 'stock.location'

    diff_level = fields.Integer('Location diff level', default=1, help="Location diff level")



