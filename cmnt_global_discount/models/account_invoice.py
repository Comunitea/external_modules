# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    global_discount = fields.Boolean('Line created by global discount')


class AccountInvoice(models.Model):
    _description = 'Invoice global discount'
    _inherit = 'account.invoice'

    gd_id = fields.Many2one('global.discount', 'Global Discount')
    discount_rate = fields.Float('Discount Rate',
                                 related='gd_id.discount_rate',
                                 readonly=True)
    amount_subtotal = fields.Float(string='Subtotal',
                                   compute='_compute_amount_no_discount',
                                   multi='sums',
                                   store=True,
                                   digits_compute=dp.get_precision('Account'))
    amount_discount = fields.Float(string='Total Global Discount',
                                   compute='_compute_amount_no_discount',
                                   multi='sums',
                                   store=True,
                                   digits_compute=dp.get_precision('Account'))

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount', 'gd_id')
    def _compute_amount_no_discount(self):
        discount_lines = self.invoice_line.filtered('global_discount')

        self.amount_discount = \
            abs(sum(discount_lines.mapped('price_subtotal')))
        self.amount_subtotal = self.amount_untaxed + self.amount_discount
        return

    @api.multi
    def write(self, vals):
        res = super(AccountInvoice, self).write(vals)
        if 'invoice_line' in vals:
            for invoice in self:
                if invoice.state == 'draft':
                    # Delete & recalculate discount lines
                    discount_lines = \
                        invoice.invoice_line.filtered('global_discount')
                    discount_lines.unlink()
                    self._create_global_discount_lines(invoice)
        return res

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice, self).create(vals)
        if 'invoice_line' in vals:
            self._create_global_discount_lines(invoice)
        return invoice

    @api.multi
    def _create_global_discount_lines(self, invoice):
        lines_by_tax = {}
        taxes_in_lines = invoice.invoice_line.mapped('invoice_line_tax_id')
        dis = invoice.discount_rate
        if not dis:
            return

        for tax in taxes_in_lines:
            if tax not in lines_by_tax:
                lines_by_tax[tax] = 0.0
            lines = invoice.invoice_line.\
                filtered(lambda r: tax in r.invoice_line_tax_id)
            lines_by_tax[tax] = sum([l.price_subtotal for l in lines])

        # Consider lines without taxes
        no_tax_lines = invoice.invoice_line.\
            filtered(lambda r: not r.invoice_line_tax_id)
        if no_tax_lines:
            lines_by_tax[False] = sum([l.price_subtotal for l in no_tax_lines])

        for tax in lines_by_tax:
            price_discounted = lines_by_tax[tax] * (dis / 100.0)
            vals = {
                'invoice_id': invoice.id,
                'name': _("Global discount line for tax %s")
                % tax.name if tax else _("Global discount line no tax"),
                'quantity': 1,
                'price_unit': -(price_discounted),
                'invoice_line_tax_id': [(6, 0, [tax.id])] if tax else False,
                'global_discount': True
            }
            self.env['account.invoice.line'].create(vals)
        return
