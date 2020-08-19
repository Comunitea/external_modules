# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class PaymentTerm(models.Model):

    _inherit = "account.payment.term"

    early_payment_discount_ids = fields.One2many(
        'account.early.payment.discount', 'payment_term_id',
        'E.P. discounts')
