from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    payment_mode_id = fields.Many2one(
        readonly=False,
    )
