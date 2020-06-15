# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp
import time

def intersect(la, lb):
    """returns True for equal keys in two lists"""
    l = filter(lambda x: x in lb, la)
    return len(l) == len(la) == len(lb)

class AccountInvoice(models.Model):

    _inherit = 'account.invoice'


    early_payment_discount = fields.Float('E.P. disc.(%)', digits=(16,2),
                                          help="Early payment discount")
    early_payment_discount_amount = fields.Float(
        'E.P. amount', digits=dp.get_precision('Account'),
        help="Early payment discount amount to apply.", readonly=True,
        compute='_compute_early_payment_discount_amount')

    @api.multi
    def _compute_early_payment_discount_amount(self):
        res = {}
        prod_early_payment_id = self.env['product.product'].search([('default_code', '=', 'DPP')])
        prod_early_payment_id = prod_early_payment_id and prod_early_payment_id[0] or False

        if prod_early_payment_id:
            for invoice in self:
                if not invoice.early_payment_discount:
                    invoice.early_payment_discount_amount = 0.0

                #searches if DPP is applied
                found = False
                for line in invoice.invoice_line_ids:
                    if line.product_id and line.product_id.id == prod_early_payment_id.id:
                        found = True
                        break;
                if not found:
                    invoice.early_payment_discount_amount = 0.0
                else:
                    total_net_price = 0.0
                    for invoice_line in invoice.invoice_line_ids:
                        if invoice_line.product_id and \
                                invoice_line.product_id.without_early_payment:
                            continue
                        total_net_price += invoice_line.price_subtotal

                    invoice.early_payment_discount_amount = float(total_net_price) - (float(total_net_price) * (1 - (invoice.early_payment_discount or 0.0) / 100.0))

    def compute_early_payment_discount(self, invoice_line_ids, early_payment_percentage):
        """computes early payment price_unit"""
        total_net_price = 0.0

        for invoice_line in self.env['account.invoice.line'].browse(invoice_line_ids):
            if invoice_line.product_id and \
                    invoice_line.product_id.without_early_payment:
                continue
            total_net_price += invoice_line.price_subtotal

        return float(total_net_price) - (float(total_net_price) * (1 - (float(early_payment_percentage) or 0.0) / 100.0))

    @api.multi
    def compute_early_payment_lines(self):
        self.ensure_one()
        early_payments = {}
        inv_lines_out_vat = []
        new_lines = self.env['account.invoice.line']

        for invoice_line in self.invoice_line_ids:
            if invoice_line.product_id and \
                    invoice_line.product_id.without_early_payment:
                continue
            if invoice_line.invoice_line_tax_ids:
                line_tax_ids = [x.id for x in invoice_line.invoice_line_tax_ids]
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
                    elif prod_early_payment.property_account_income_id \
                            and str(
                                prod_early_payment.property_account_income_id.id) not in group_account_line[early_payment_line]:
                        group_account_line[early_payment_line][str(
                            prod_early_payment.property_account_income_id.id
                        )] = [invoice_line.id]
                    elif prod_early_payment.property_account_income_id and str(prod_early_payment.property_account_income_id.id) in group_account_line[early_payment_line] or prod_early_payment.categ_id.property_account_sale_early_payment_disc.id and str(prod_early_payment.categ_id.property_account_sale_early_payment_disc.id) in group_account_line[early_payment_line]:
                        if prod_early_payment.property_account_income_id:
                            group_account_line[early_payment_line][str(prod_early_payment.property_account_income_id.id)].append(invoice_line.id)
                        else:
                            group_account_line[early_payment_line][str(prod_early_payment.categ_id.property_account_sale_early_payment_disc.id)].append(invoice_line.id)
                    else:
                        raise exceptions.except_orm(_('Warning'), _('Cannot set early payment discount because now is impossible find the early payment account. Review invoice products categories have defined early payment account by default or early payment discount product have defined an output account.'))

            partner_id = self.partner_id and self.partner_id.id or False
            for early_payment_line in group_account_line:
                for account_id in group_account_line[early_payment_line]:
                    new_lines += self.env['account.invoice.line'].with_context(partner_id=partner_id).create({
                        'name': _("Early payment discount") + " " + str(self.early_payment_discount) + "%",
                        'invoice_id': self.id,
                        'product_id': prod_early_payment.id,
                        'account_id': int(account_id),
                        'price_unit': self.currency_id.round(0.0 - (self.compute_early_payment_discount(group_account_line[early_payment_line][account_id], self.early_payment_discount))),
                        'quantity': 1,
                        'invoice_line_tax_ids': [(6, 0, [int(x) for x in early_payment_line.split(',')])],
                        'account_analytic_id': analytic_id
                        })

            if inv_lines_out_vat:
                new_lines += self.env['account.invoice.line'].with_context(partner_id=partner_id).create({
                        'name': _("Early payment discount") + " " + str(self.early_payment_discount) + "%",
                        'invoice_id': self.id,
                        'product_id': prod_early_payment.id,
                        'account_id':
                            prod_early_payment.property_account_income_id.id
                            or prod_early_payment.categ_id and
                            prod_early_payment.categ_id.property_account_sale_early_payment_disc.id ,
                        'price_unit': self.currency_id.round(0.0 - (self.compute_early_payment_discount(inv_lines_out_vat, self.early_payment_discount))),
                        'quantity': 1,
                        'account_analytic_id': analytic_id
                        })

        #recompute taxes
        self._compute_amount()
        self.compute_taxes()

        return new_lines

    @api.multi
    def button_compute_early_payment_disc(self):
        for invoice in self:
            if invoice.early_payment_discount:
                orig_early_payment_lines = invoice.env['account.invoice.line']
                early_payment = invoice.env['product.product'].search([('default_code', '=', 'DPP')])

                for invoice_line in invoice.invoice_line_ids:
                    if invoice_line.product_id.id == early_payment.id:
                        orig_early_payment_lines += invoice_line

                if orig_early_payment_lines:
                    #delete old early payment lines
                    orig_early_payment_lines.unlink()

                invoice.compute_early_payment_lines()
        return True


    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
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
                    early_discs = self.env['account.early.payment.discount'].search([('partner_id', '=', False), ('payment_term_id', '=', self.payment_term_id.id)])
                    if early_discs:
                        self.early_payment_discount = early_discs[0].early_payment_discount
        return res

    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):
        res = super(AccountInvoice, self)._onchange_payment_term_date_invoice()
        if not self.payment_term_id:
            self.early_payment_discount = False
        commercial_partner = self.partner_id.commercial_partner_id
        early_discs = commercial_partner.early_payment_discount_ids.filtered(lambda x: x.payment_term_id == self.payment_term_id)
        if early_discs:
            self.early_payment_discount = early_discs[0].early_payment_discount
        else:
            early_discs = self.env['account.early.payment.discount'].search([('partner_id', '=', False), ('payment_term_id', '=', self.payment_term_id.id)])
            if early_discs:
                self.early_payment_discount = early_discs[0].early_payment_discount
        return res
