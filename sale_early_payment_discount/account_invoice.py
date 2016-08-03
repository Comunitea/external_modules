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
from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp
import time

def intersect(la, lb):
    """returns True for equal keys in two lists"""
    l = filter(lambda x: x in lb, la)
    return len(l) == len(la) == len(lb)

class account_invoice(models.Model):
    """Inherit account_invoice to compute from button the early payment
       discount"""

    _inherit = 'account.invoice'

    @api.one
    def _get_early_discount_amount(self):
        """obtain early_payment_discount_amount"""
        res = {}
        prod_early_payment_id = self.env['product.product'].search([('default_code', '=', 'DPP')])
        prod_early_payment_id = prod_early_payment_id and prod_early_payment_id[0] or False

        if prod_early_payment_id:
            #for invoice in self.browse(cr, uid, ids):
            if not self.early_payment_discount:
                self.early_payment_discount_amount = 0.0

            #searches if DPP is applied
            found = False
            for line in self.invoice_line:
                if line.product_id and line.product_id.id == prod_early_payment_id.id:
                    found = True
                    break;

            if found:
                self.early_payment_discount_amount = 0.0
            else:
                total_net_price = 0.0
                for invoice_line in self.invoice_line:
                    total_net_price += invoice_line.price_subtotal

                self.early_payment_discount_amount = float(total_net_price) - (float(total_net_price) * (1 - (self.early_payment_discount or 0.0) / 100.0))

    early_payment_discount = fields.Float('E.P. disc.(%)', digits=(16,2),
                                          help="Early payment discount")
    early_discount_amount = fields.Float('E.P. amount', digits_compute=dp.get_precision('Account'), help="Early payment discount amount to apply.", readonly=True, compute=_get_early_discount_amount)

    def compute_early_payment_discount(self, invoice_line_ids, early_payment_percentage):
        """computes early payment price_unit"""
        total_net_price = 0.0

        for invoice_line in self.env['account.invoice.line'].browse(invoice_line_ids):
            total_net_price += invoice_line.price_subtotal

        return float(total_net_price) - (float(total_net_price) * (1 - (float(early_payment_percentage) or 0.0) / 100.0))

    @api.one
    def compute_early_payment_lines(self):
        """creates early payment lines"""
        early_payments = {}
        inv_lines_out_vat = []

        for invoice_line in self.invoice_line:
            if invoice_line.invoice_line_tax_id:
                line_tax_ids = [x.id for x in invoice_line.invoice_line_tax_id]
                found = False

                for key in early_payments:
                    if intersect([int(x) for x in key.split(",")], line_tax_ids):
                        early_payments[key].append(invoice_line.id)
                        found = True
                        break;

                if not found:
                    tax_str = ",".join([str(x) for x in line_tax_ids])
                    early_payments[tax_str] = [invoice_line.id]
            else:
                #lines without vat defined
                inv_lines_out_vat.append(invoice_line.id)

        prod_early_payment = self.env['product.product'].search([('default_code', '=', 'DPP')])
        prod_early_payment = prod_early_payment and prod_early_payment[0] or False

        if prod_early_payment:
            analytic_id = False
            rec = self.env['account.analytic.default'].account_get(prod_early_payment.id, self.partner_id.id, self._uid, time.strftime('%Y-%m-%d'), company_id=self.company_id.id)
            if rec:
                analytic_id = rec.analytic_id.id
            group_account_line = {}
            for early_payment_line in early_payments:
                group_account_line[early_payment_line] = {}

                for invoice_line in self.env['account.invoice.line'].browse(early_payments[early_payment_line]):
                    if invoice_line.product_id.categ_id and invoice_line.product_id.categ_id.property_account_sale_early_payment_disc and str(invoice_line.product_id.categ_id.property_account_sale_early_payment_disc.id) not in group_account_line[early_payment_line]:
                        group_account_line[early_payment_line][str(invoice_line.product_id.categ_id.property_account_sale_early_payment_disc.id)] = [invoice_line.id]
                    elif invoice_line.product_id.categ_id and invoice_line.product_id.categ_id.property_account_sale_early_payment_disc and str(invoice_line.product_id.categ_id.property_account_sale_early_payment_disc.id) in group_account_line[early_payment_line]:
                        group_account_line[early_payment_line][str(invoice_line.product_id.categ_id.property_account_sale_early_payment_disc.id)].append(invoice_line.id)
                    elif prod_early_payment.property_stock_account_output and str(prod_early_payment.property_stock_account_output.id) not in group_account_line[early_payment_line]:
                        group_account_line[early_payment_line][str(prod_early_payment.property_stock_account_output.id)] = [invoice_line.id]
                    elif prod_early_payment.property_stock_account_output and str(prod_early_payment.property_stock_account_output.id) in group_account_line[early_payment_line] or prod_early_payment.categ_id.property_account_sale_early_payment_disc.id and str(prod_early_payment.categ_id.property_account_sale_early_payment_disc.id) in group_account_line[early_payment_line]:
                        group_account_line[early_payment_line][str(prod_early_payment.property_stock_account_output.id)].append(invoice_line.id)
                    else:
                        raise exceptions.except_orm(_('Warning'), _('Cannot set early payment discount because now is impossible find the early payment account. Review invoice products categories have defined early payment account by default or early payment discount product have defined an output account.'))

            partner_id = self.partner_id and self.partner_id.id or False
            for early_payment_line in group_account_line:
                for account_id in group_account_line[early_payment_line]:
                    self.env['account.invoice.line'].with_context(partner_id=partner_id).create({
                        'name': _("Early payment discount") + " " + str(self.early_payment_discount) + "%",
                        'invoice_id': self.id,
                        'product_id': prod_early_payment.id,
                        'account_id': int(account_id),
                        'price_unit': 0.0 - (self.compute_early_payment_discount(group_account_line[early_payment_line][account_id], self.early_payment_discount)),
                        'quantity': 1,
                        'invoice_line_tax_id': [(6, 0, [int(x) for x in early_payment_line.split(',')])],
                        'account_analytic_id': analytic_id
                        })

            if inv_lines_out_vat:
                self.env['account.invoice.line'].with_context(partner_id=partner_id).create({
                        'name': _("Early payment discount") + " " + str(self.early_payment_discount) + "%",
                        'invoice_id': self.id,
                        'product_id': prod_early_payment.id,
                        'account_id': prod_early_payment.categ_id and prod_early_payment.categ_id.property_account_sale_early_payment_disc.id or prod_early_payment.property_stock_account_output.id,
                        'price_unit': 0.0 - (self.compute_early_payment_discount(inv_lines_out_vat, self.early_payment_discount)),
                        'quantity': 1,
                        'account_analytic_id': analytic_id
                        })

        #recompute taxes
        self.button_compute(set_total=(type in ('in_invoice', 'in_refund')))

        return True

    @api.one
    def button_compute_early_payment_disc(self):
        """computes early payment discount in invoice"""

        #for invoice in self.browse(cr, uid, ids):
        if self.early_payment_discount:
            #create list with all early discount lines to delete, new early discount lines will be created
            orig_early_payment_lines = self.env['account.invoice.line']
            #searches for early discount product
            early_payment = self.env['product.product'].search([('default_code', '=', 'DPP')])

            for invoice_line in self.invoice_line:
                if invoice_line.product_id.id == early_payment.id:
                    orig_early_payment_lines += invoice_line

            if orig_early_payment_lines:
                #delete old early payment lines
                orig_early_payment_lines.unlink()

            self.compute_early_payment_lines()
        return True

    def onchange_partner_id(self, cr, uid, ids, type, partner_id, date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False, context=False):
        """extend this event for delete early payment discount if it isn't valid to new partner or add new early payment discount"""
        res = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id, date_invoice=date_invoice, payment_term=payment_term, partner_bank_id=partner_bank_id, company_id=company_id, context=context)
        if not partner_id:
            res['value']['early_payment_discount'] = False
            return res

        early_discs = []

        if not payment_term and not (res.get('value') and res['value'].get('payment_term')):
            early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', partner_id), ('payment_term_id', '=', False)], context=context)
            if early_discs:
                res['value']['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0], context).early_payment_discount
        elif payment_term and not (res.get('value') and res['value'].get('payment_term')):
            early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', partner_id), ('payment_term_id', '=', payment_term)], context=context)
            if early_discs:
                res['value']['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0], context).early_payment_discount
            else:
                early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', False), ('payment_term_id', '=', payment_term)], context=context)
                if early_discs:
                    res['value']['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0], context).early_payment_discount
        elif res.get('value') and res['value'].get('payment_term'):
            early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', partner_id), '|',('payment_term_id', '=', res['value']['payment_term']), ('payment_term_id', '=', False)], context=context)
            if early_discs:
                res['value']['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0], context).early_payment_discount
            else:
                early_discs = self.pool.get('account.partner.payment.term.early.discount').search(cr, uid, [('partner_id', '=', False), ('payment_term_id', '=', res['value']['payment_term'])], context=context)
                if early_discs:
                    res['value']['early_payment_discount'] = self.pool.get('account.partner.payment.term.early.discount').browse(cr, uid, early_discs[0], context).early_payment_discount

        return res

    @api.onchange('payment_term')
    def onchange_payment_term(self):
        """onchange event to update early payment discount when the payment
            term changes"""
        early_disc_obj = self.env['account.partner.payment.term.early.discount']
        if not self.payment_term:
            self.early_payment_discount = False
            return

        self.date_due = False

        early_discs = early_disc_obj.search([('partner_id', '=', self.partner_id.id), ('payment_term_id', '=', self.payment_term.id)])
        if early_discs:
            self.early_payment_discount = early_discs.early_payment_discount
        else:
            early_discs = early_disc_obj.search([('partner_id', '=', False), ('payment_term_id', '=', self.payment_term.id)])
            if early_discs:
                self.early_payment_discount = early_discs.early_payment_discount
