from odoo import _, api, fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    show_prices = fields.Boolean(string="Show Prices", default=False)
