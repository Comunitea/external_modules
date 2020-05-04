# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrde(models.Model):

    _inherit = "sale.order"

    prestashop_state = fields.Many2one("sale.order.state")
