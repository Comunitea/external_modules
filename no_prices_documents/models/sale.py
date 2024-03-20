from odoo import _, api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    show_prices = fields.Boolean(string="Show Prices", default=False)
