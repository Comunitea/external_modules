# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""Inherit sale_order to add early payment discount"""

from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp


class sale_order(models.Model):
    """Inherit sale_order to add early payment discount"""

    _inherit = 'sale.order'

    early_payment_discount = fields.Float('E.P. disc.(%)', digits=(16,2), help="Early payment discount")
    early_payment_disc_total = fields.Float('With E.P.', digits_compute=dp.get_precision('Account'), compute='_amount_all2')
    early_payment_disc_untaxed = fields.Float('Untaxed Amount E.P.', digits_compute=dp.get_precision('Account'), compute='_amount_all2')
    early_payment_disc_tax = fields.Float('Taxes E.P.', digits_compute=dp.get_precision('Account'), compute='_amount_all2')
    total_early_discount = fields.Float('E.P. amount', digits_compute=dp.get_precision('Account'), compute='_amount_all2')

    @api.one
    @api.depends('order_line', 'early_payment_discount',
                 'order_line.price_unit', 'order_line.tax_id',
                 'order_line.discount', 'order_line.product_uom_qty')
    def _amount_all2(self):
        """calculates functions amount fields"""
        if not self.early_payment_discount:
            self.early_payment_disc_total = self.amount_total
            self.early_payment_disc_tax = self.amount_tax
            self.early_payment_disc_untaxed = self.amount_untaxed
        else:
            self.early_payment_disc_tax = self.amount_tax * (1.0 - (float(self.early_payment_discount or 0.0)) / 100.0)
            self.early_payment_disc_untaxed = self.amount_untaxed * (1.0 - (float(self.early_payment_discount or 0.0)) / 100.0)
            self.early_payment_disc_total = self.early_payment_disc_untaxed + self.early_payment_disc_tax
            self.total_early_discount = self.early_payment_disc_untaxed - self.amount_untaxed

    def onchange_partner_id2(self, cr, uid, ids, part, early_payment_discount=False, payment_term=False, context=None):
        """extend this event for delete early payment discount if it isn't valid to new partner or add new early payment discount"""
        res = self.onchange_partner_id(cr, uid, ids, part, context)
        if not part:
            res['value']['early_payment_discount'] = False
            return res
        partner = self.pool.get('res.partner').browse(cr, uid, part, context)
        com_part_id = partner.commercial_partner_id.id
        early_discs = []

        if not early_payment_discount and res.get('value', False):
            if not payment_term:
                early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', com_part_id), ('payment_term_id', '=', False)], context=context)
                if early_discs:
                    res['value']['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0], context).early_payment_discount

            if res['value'].get('payment_term', False):
                payment_term = res['value']['payment_term']

            if payment_term or not early_discs:
                early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', com_part_id), ('payment_term_id', '=', payment_term)], context=context)
                if early_discs:
                    res['value']['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0], context).early_payment_discount
                else:
                    early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', False), ('payment_term_id', '=', payment_term)], context=context)
                    if early_discs:
                        res['value']['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0], context).early_payment_discount

        return res

    def onchange_payment_term(self, cr, uid, ids, payment_term, part=False):
        """onchange event to update early payment dicount when the payment term changes"""
        res = {}
        if not payment_term:
            res['early_payment_discount'] = False
            return {'value': res}
        partner = self.pool.get('res.partner').browse(cr, uid, part, context)
        com_part_id = partner.commercial_partner_id.id
        early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', com_part_id), ('payment_term_id', '=', payment_term)])
        if early_discs:
            res['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0]).early_payment_discount
        else:
            early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', False), ('payment_term_id', '=', payment_term)])
            if early_discs:
                res['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0]).early_payment_discount

        return {'value': res}

    @api.multi
    def action_invoice_create(self, grouped=False, states=['confirmed', 'done', 'exception'], date_invoice=False):
        """
        Inherited method for writing early_payment_discount value in created invoice
        """
        invoice_id = super(sale_order, self).action_invoice_create(grouped=grouped, states=states, date_invoice = date_invoice)
        invoice = self.env['account.invoice'].browse(invoice_id)
        current_sale = self and self[0] or False
        if current_sale.early_payment_discount:
            invoice.write({'early_payment_discount': current_sale.early_payment_discount})
        return invoice_id
