# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_type = fields.Selection([('percent', 'Percentage'),
                                      ('amount', 'Amount')],
                                     string='Discount Type',
                                     help='Select discount type',
                                     default='percent')
    discount_rate = fields.Float('Discount Rate')
    amount_untaxed = fields.Float(string='Untaxed Amount',
                                  compute='_amount_all',
                                  multi='sums',
                                  track_visibility='always',
                                  store=True,
                                  digits_compute=dp.get_precision('Account'),
                                  help="The amount without tax.")
    amount_tax = fields.Float(string='Taxes',
                              compute='_amount_all',
                              multi='sums',
                              track_visibility='always',
                              store=True,
                              digits_compute=dp.get_precision('Account'),
                              help="The tax amount.")
    amount_total = fields.Float(string='Total',
                                compute='_amount_all',
                                multi='sums',
                                track_visibility='always',
                                store=True,
                                digits_compute=dp.get_precision('Account'),
                                help="The total amount")
    amount_subtotal = fields.Float(string='Subtotal',
                                   compute='_amount_all',
                                   multi='sums',
                                   store=True,
                                   digits_compute=dp.get_precision('Account'))
    amount_discount = fields.Float(string='Total Global Discount',
                                   compute='_amount_all',
                                   multi='sums',
                                   store=True,
                                   digits_compute=dp.get_precision('Account'))

    @api.depends('order_line.price_subtotal', 'discount_rate', 'discount_type')
    def _amount_all(self):
        for order in self:
            cur = order.pricelist_id.currency_id
            amount_untaxed = amount_tax = 0.0
            amount_subtotal = amount_discount = 0.0
            for line in order.order_line:
                amount_subtotal += line.price_subtotal
                amount_tax += order._amount_line_tax(line)

            if order.discount_type == 'percent':
                amount_discount = amount_subtotal * self.discount_rate / 100
            else:
                amount_discount = self.discount_rate
            amount_untaxed = amount_subtotal - amount_discount
            amount_total = amount_untaxed + amount_tax
            order.update({
                'amount_untaxed': cur.round(amount_untaxed),
                'amount_tax': cur.round(amount_tax),
                'amount_total': cur.round(amount_total),
                'amount_subtotal': cur.round(amount_subtotal),
                'amount_discount': cur.round(amount_discount),
            })

    @api.model
    def _prepare_invoice(self):
        """
        This method send the discount_type, discount_rate and amount_discount
        to the account.invoice model
        """
        res = super(SaleOrder, self)._prepare_invoice()
        res['discount_type'] = self.discount_type
        res['discount_rate'] = self.discount_rate
        return res

    @api.multi
    def onchange_partner_id(self, part):
        res = super(SaleOrder, self).onchange_partner_id(part)
        partner = self.env['res.partner'].browse(part)
        if partner.discount_type:
            res['value']['discount_type'] = partner.discount_type
        if partner.discount_rate:
            res['value']['discount_rate'] = partner.discount_rate
        return res
