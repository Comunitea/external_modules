# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _description = 'Invoice global discount'
    _inherit = 'account.invoice'

    amount_untaxed = fields.Float(string='Subtotal',
                                  digits=dp.get_precision('Account'),
                                  store=True, readonly=True,
                                  compute='_compute_amount',
                                  track_visibility='always')
    amount_tax = fields.Float(string='Tax',
                              digits=dp.get_precision('Account'),
                              store=True,
                              readonly=True,
                              compute='_compute_amount')
    amount_total = fields.Float(string='Total',
                                digits=dp.get_precision('Account'),
                                store=True,
                                readonly=True,
                                compute='_compute_amount')
    gd_id = fields.Many2one('global.discount', 'Global Discount')

    discount_type = fields.Selection([('percent', 'Percentage'),
                                      ('amount', 'Amount')],
                                     string='Discount Type',
                                     help='Select discount type',
                                     default='percent',
                                     related='gd_id.discount_type',
                                     readonly=True)
    discount_rate = fields.Float('Discount Rate',
                                 related='gd_id.discount_rate',
                                 readonly=True)
    amount_subtotal = fields.Float(string='Subtotal',
                                   compute='_compute_amount',
                                   multi='sums',
                                   store=True,
                                   digits_compute=dp.get_precision('Account'))
    amount_discount = fields.Float(string='Total Global Discount',
                                   compute='_compute_amount',
                                   multi='sums',
                                   store=True,
                                   digits_compute=dp.get_precision('Account'))

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount',
                 'gd_id')
    def _compute_amount(self):
        self.amount_subtotal = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_tax = sum(line.amount for line in self.tax_line)
        if self.gd_id:
            if self.discount_type == 'percent':
                self.amount_discount = self.amount_subtotal * self.discount_rate / 100
                self.amount_tax = \
                    self.amount_tax * (1 - self.discount_rate / 100)
            else:
                self.amount_discount = self.discount_rate
                self.amount_tax = self.amount_tax - self.amount_discount
        self.amount_untaxed = self.amount_subtotal - self.amount_discount
        self.amount_total = self.amount_untaxed + self.amount_tax



    # @api.one
    # @api.depends(
    #     'state', 'currency_id', 'invoice_line_ids.price_subtotal',
    #     'move_id.line_ids.amount_residual',
    #     'move_id.line_ids.currency_id')
    # def _compute_residual(self):
    #     residual = 0.0
    #     residual_company_signed = 0.0
    #     sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
    #     for line in self.sudo().move_id.line_ids:
    #         if line.account_id.internal_type in ('receivable', 'payable'):
    #             residual_company_signed += line.amount_residual
    #             if line.currency_id == self.currency_id:
    #                 residual += line.amount_residual_currency if line.currency_id else line.amount_residual
    #             else:
    #                 from_currency = (line.currency_id and line.currency_id.with_context(date=line.date)) or line.company_id.currency_id.with_context(date=line.date)
    #                 residual += from_currency.compute(line.amount_residual, self.currency_id)
    #     self.residual_company_signed = abs(residual_company_signed) * sign - self.amount_discount
    #     self.residual_signed = abs(residual) * sign - self.amount_discount
    #     self.residual = abs(residual) - self.amount_discount
    #     digits_rounding_precision = self.currency_id.rounding
    #     if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
    #         self.reconciled = True
    #     else:
    #         self.reconciled = False