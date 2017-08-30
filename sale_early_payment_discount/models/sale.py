# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    early_payment_discount = fields.Float('E.P. disc.(%)', digits=(16,2), help="Early payment discount")
    early_payment_disc_total = fields.Float('With E.P.', digits=dp.get_precision('Account'), compute='_amount_all')
    early_payment_disc_untaxed = fields.Float('Untaxed Amount E.P.', digits=dp.get_precision('Account'), compute='_amount_all')
    early_payment_disc_tax = fields.Float('Taxes E.P.', digits=dp.get_precision('Account'), compute='_amount_all')
    total_early_discount = fields.Float('E.P. amount', digits=dp.get_precision('Account'), compute='_amount_all')

    @api.depends('order_line.price_total', 'early_payment_discount')
    def _amount_all(self):
        super(SaleOrder, self)._amount_all()
        if not self.early_payment_discount:
            self.early_payment_disc_total = self.amount_total
            self.early_payment_disc_tax = self.amount_tax
            self.early_payment_disc_untaxed = self.amount_untaxed
        else:
            cur = self.pricelist_id.currency_id
            val = val1 = 0
            for line in self.order_line:
                if line.product_id and line.product_id.without_early_payment:
                    val1 += line.price_subtotal
                    val += line.price_tax
                else:
                    val1 += line.price_subtotal * \
                        (1.0 - (float(self.early_payment_discount or 0.0)) /
                         100.0)
                    val += line.price_tax * \
                        (1.0 - (float(self.early_payment_discount or 0.0)) /
                         100.0)
            self.early_payment_disc_tax = cur.round(val)
            self.early_payment_disc_untaxed = cur.round(val1)
            self.early_payment_disc_total = cur.round(val+val1)
            self.total_early_discount = self.early_payment_disc_untaxed - \
                self.amount_untaxed

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        if not self.partner_id:
            self.early_payment_discount = False
            return res
        commercial_partner = self.partner_id.commercial_partner_id
        if not self.early_payment_discount:
            if not self.payment_term_id:
                early_discs = commercial_partner.early_payment_discount_ids
                if early_discs:
                    self.early_payment_discount = early_discs[0].early_payment_discount

            else:
                early_discs = commercial_partner.early_payment_discount_ids.filtered(lambda x: x.payment_term_id == self.payment_term_id)
                if early_discs:
                    self.early_payment_discount = early_discs[0].early_payment_discount
                else:
                    early_discs = commercial_partner.early_payment_discount_ids
                    if early_discs:
                        self.early_payment_discount = early_discs[0].early_payment_discount
                    else:
                        early_discs = self.env['account.early.payment.discount'].search([('partner_id', '=', False), ('payment_term_id', '=', self.payment_term_id.id)])
                        if early_discs:
                            self.early_payment_discount = early_discs[0].early_payment_discount
        return res

    @api.onchange('payment_term_id')
    def onchange_payment_term(self):
        if not self.payment_term_id:
            self.early_payment_discount = False
            return
        commercial_partner = self.partner_id.commercial_partner_id
        early_discs = commercial_partner.early_payment_discount_ids.filtered(lambda x: x.payment_term_id == self.payment_term_id)
        if early_discs:
            self.early_payment_discount = early_discs[0].early_payment_discount
        else:
            early_discs = commercial_partner.early_payment_discount_ids
            if early_discs:
                self.early_payment_discount = early_discs[0].early_payment_discount
            else:
                early_discs = self.env['account.early.payment.discount'].search([('partner_id', '=', False), ('payment_term_id', '=', self.payment_term_id.id)])
                if early_discs:
                    self.early_payment_discount = early_discs[0].early_payment_discount

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['early_payment_discount'] = self.early_payment_discount
        return res
