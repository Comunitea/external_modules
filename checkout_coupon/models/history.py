# -*- coding: utf-8 -*-
# © 2018 Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class CouponsHistory(models.Model):
    _name = "checkout_coupon.history"

    name = fields.Many2one("checkout_coupon.coupons", string="Coupone name")
    code = fields.Char(related="name.code", string="Code", readonly=True)
    order = fields.Many2one("sale.order", string="Order")
    partner = fields.Many2one("res.partner", related="order.partner_id", string="Partner", readonly=True)
    date = fields.Datetime(related="order.date_order", string="Order date", readonly=True)
    currency_id = fields.Many2one("res.currency", related="order.currency_id")
    cart_total = fields.Monetary(related="order.amount_total", currency_field="currency_id",
                                 string="Order amount total", readonly=True)
