# -*- coding: utf-8 -*-
# Copyright 2015 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    @api.one
    def _get_amount_residual(self):
        advance_amount = 0.0
        for line in self.account_payment_ids:
            if line.state != 'draft':
                advance_amount += line.amount
        self.amount_resisual = self.amount_total - advance_amount

    account_payment_ids = fields.One2many('account.payment', 'purchase_id',
                                          string="Pay purchase advanced")
    amount_resisual = fields.Float('Residual amount', readonly=True,
                                   compute="_get_amount_residual")
