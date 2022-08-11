from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    payment_mode_id = fields.Many2one(
        comodel_name="account.payment.mode",
        readonly=False,
        compute=False
    )

    def _compute_payment_mode(self):
        for line in self:
            if line.account_internal_type in (
                "receivable",
                "payable",
            ):
                line.payment_mode_id = line.move_id.payment_mode_id
            else:
                line.payment_mode_id = False
