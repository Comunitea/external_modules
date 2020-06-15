# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.onchange('purchase_id')
    def purchase_order_change(self):
        """
        Set purchase early discount when create a invoice from smart button
        """
        early_disc = 0
        if not self.early_payment_discount:
            early_disc = self.purchase_id.early_payment_discount
        res = super(AccountInvoice, self).purchase_order_change()
        self.early_payment_discount = early_disc
        return res
    

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        """
        Avoid early_payment_discount to be false if exist early_discount
        and is a purchase invoice. It is to avoid the purchase_order_change
        being overwritted by this onchange
        """
        early_disc = self.early_payment_discount
        res = super(AccountInvoice, self)._onchange_partner_id()
        if early_disc and self.type == 'in_invoice':
            self.early_payment_discount = early_disc
        return res

    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):
        """
        Avoid early_payment_discount to be false if exist early_discount
        and is a purchase invoice. It is to avoid the purchase_order_change
        being overwritted by this onchange
        """
        early_disc = self.early_payment_discount
        res = super(AccountInvoice, self)._onchange_payment_term_date_invoice()
        if early_disc and self.type == 'in_invoice':
            self.early_payment_discount = early_disc
        return res
  