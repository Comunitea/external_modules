# -*- coding: utf-8 -*-
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).ls.

from odoo import api, fields, models


class SaleOrder(models.Model):
    """
        Redefine model to show cash on delivery amount in cart total
    """
    _inherit = 'sale.order'

    amount_cash_on_delivery = fields.Monetary(
        compute='_compute_amount_cash_on_delivery', digits=0,
        string='Cash on Delivery Amount',
        help="The amount without tax.", store=True, track_visibility='always')
    has_cash_on_delivery = fields.Boolean(
        compute='_compute_has_cash_on_delivery', string='Has cash on delivery',
        help="Has an order line set for cash on delivery", store=True)

    @api.depends('order_line.price_unit', 'order_line.tax_id', 'order_line.discount', 'order_line.product_uom_qty')
    def _compute_amount_cash_on_delivery(self):
        for order in self:
            if self.env.user.has_group('sale.group_show_price_subtotal'):
                order.amount_cash_on_delivery = sum(order.order_line.filtered('payment_fee_line')
                                                    .mapped('price_subtotal'))
            else:
                order.amount_cash_on_delivery = sum(order.order_line.filtered('payment_fee_line')
                                                    .mapped('price_total'))

    @api.depends('order_line.payment_fee_line')
    def _compute_has_cash_on_delivery(self):
        for order in self:
            order.has_cash_on_delivery = any(order.order_line.filtered('payment_fee_line'))

    def update_fee_line(self, acquirer):
        """
        Update fee line depending on the context for do not delete fee lines for default payment method.
        :param acquirer:
        :return:
        """
        if self._context.get('no_update_fee_line', False):
            return
        return super(SaleOrder, self).update_fee_line(acquirer)

    @api.multi
    @api.depends('website_order_line.product_uom_qty', 'website_order_line.product_id', 'website_order_line')
    def _compute_cart_info(self):
        """
        For not compute payment fee as quantity in header icon because is not a real product
        and do not want to sum payment fee as quantity.
        :return: default values less payment fee as quantity.
        """
        for order in self:
            order.cart_quantity = int(sum(order.website_order_line.filtered(lambda x: not x.payment_fee_line)
                                          .mapped('product_uom_qty')))
            order.only_services = all(l.product_id.type in ('service', 'digital') for l in order.website_order_line
                                      .filtered(lambda x: not x.payment_fee_line))

    @api.depends('order_line.price_unit', 'order_line.tax_id', 'order_line.discount', 'order_line.product_uom_qty')
    def _compute_amount_delivery(self):
        """
        For not compute payment fee as amount delivery for to sum into delivery.
        :return: default values less payment fee as amount delivery.
        """
        for order in self:
            if self.env.user.has_group('sale.group_show_price_subtotal'):
                order.amount_delivery = sum(order.order_line.filtered('is_delivery')
                                            .filtered(lambda x: not x.payment_fee_line).mapped('price_subtotal'))
            else:
                order.amount_delivery = sum(order.order_line.filtered('is_delivery')
                                            .filtered(lambda x: not x.payment_fee_line).mapped('price_total'))
