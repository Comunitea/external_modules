# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class res_partner(models.Model):

    _inherit = "res.partner"

    early_payment_discount_ids = fields.One2many(
        'account.early.payment.discount', 'partner_id',
        'E.P. discounts')
