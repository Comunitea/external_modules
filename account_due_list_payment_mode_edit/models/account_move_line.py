from odoo import fields, models

PAYMENT_MODE_MAPPING = {
    "payable": "outbound",
    "receivable": "inbound",
}

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    payment_mode_id = fields.Many2one(
        readonly=False,
    )

    payment_mode_type = fields.Char(
        compute="_compute_payment_mode_type",
        help="""
        Technical field that enables payment mode restricted selection
        depending on due type (payable or receivable)
        """,
    )

    def _compute_payment_mode_type(self):
        for move_line in self:
            move_line.payment_mode_type = PAYMENT_MODE_MAPPING.get(
                move_line.account_internal_type, "other"
            )
