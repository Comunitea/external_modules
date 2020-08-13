# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ResPartner(models.Model):

    _inherit = "res.partner"

    early_payment_discount_ids = fields.One2many(
        'account.early.payment.discount', 'partner_id',
        'E.P. discounts')
