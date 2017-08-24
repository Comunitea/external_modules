# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountEarlyPaymentDiscount(models.Model):

    _name = "account.early.payment.discount"
    _description = "Early payment discounts"

    @api.model
    def _get_default_partner(self):
        return self.env.context.get('partner_id', False)

    @api.model
    def _get_default_payment_term(self):
        return self.env.context.get('payment_term', False)

    name = fields.Char('Name', size=64, required=True)
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 default=_get_default_partner)
    payment_term_id = fields.Many2one('account.payment.term', 'Payment Term',
                                      default=_get_default_payment_term)
    early_payment_discount = fields.Float(
        'E.P. disc.(%)', digits=(16, 2), required=True,
        help="Percentage of discount for early payment.")
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.user.company_id)
