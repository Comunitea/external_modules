# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    gd_id = fields.Many2one('global.discount', 'Global Discount')
    discount_rate = fields.Float('Discount Rate',
                                 related='gd_id.discount_rate',
                                 readonly=True)
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

    @api.depends('order_line.price_subtotal', 'gd_id')
    def _amount_all(self):
        for order in self:
            cur = order.pricelist_id.currency_id
            amount_untaxed = amount_tax = 0.0
            amount_subtotal = amount_discount = 0.0
            for line in order.order_line:
                amount_subtotal += line.price_subtotal
                amount_tax += order._amount_line_tax(line)
                if order.gd_id:
                    amount_tax = amount_tax * (1 - order.discount_rate / 100)
                    amount_tax = amount_tax - order.discount_rate
            amount_untaxed = amount_subtotal - amount_discount

            if order.gd_id:
                amount_discount = amount_subtotal * order.discount_rate / 100
                amount_discount = order.discount_rate
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
    def _prepare_invoice(self, order, lines):
        """
        This method send discount_rate and amount_discount
        to the account.invoice model
        """
        res = super(SaleOrder, self)._prepare_invoice(order, lines)
        if order.gd_id:
            res['gd_id'] = order.gd_id.id
        return res

    @api.multi
    def onchange_partner_id(self, part):
        res = super(SaleOrder, self).onchange_partner_id(part)
        partner = self.env['res.partner'].browse(part)
        if partner.gd_id:
            res['value']['gd_id'] = partner.gd_id.id
        return res
