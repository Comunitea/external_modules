# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    min_amount_required = fields.Integer(string='Minimum Amount Required', default=0,
                                         help='Set an amount if you want establish a minimum amount to show this \
                                         payment method in your website')
    max_amount_required = fields.Integer(string='Maximum Amount Required', default=0,
                                         help='Set an amount if you want establish a maximum amount to show this \
                                         payment method in your website')

