import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    payment_mode_id = fields.Many2one(
        comodel_name="account.payment.mode", string="Payment Mode"
    )
