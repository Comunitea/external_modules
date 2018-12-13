# -*- coding: utf-8 -*-
# © 2018 Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    applied_coupon = fields.Many2one("checkout_coupon.coupons", string="Applied coupon")
    total_coupon_discount = fields.Monetary(
        compute='_compute_total_coupon_discount',
        digits=0,
        string='Total coupon discount',
        store=True,
        track_visibility='always'
    )

    @api.depends('order_line.product_uom_qty')
    def _compute_total_coupon_discount(self):
        for order in self:
            order.total_coupon_discount = sum(order.order_line
                                              .filtered(lambda x: x.product_id.default_code == order.applied_coupon.code)
                                              .mapped('price_subtotal'))

    @api.multi
    @api.depends('website_order_line.product_uom_qty', 'website_order_line.product_id', 'website_order_line')
    def _compute_cart_info(self):
        for order in self:
            order.cart_quantity = int(sum(order.website_order_line
                                          .filtered(lambda x: x.product_id.sale_ok and not x.payment_fee_line)
                                          .mapped('product_uom_qty')))
