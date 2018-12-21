# -*- coding: utf-8 -*-
# © 2018 Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import string
import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Coupons(models.Model):
    _name = "checkout_coupon.coupons"

    def code_generate(self):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(10))

    _sql_constraints = [
        ("name_uniq", "unique (code)", "The coupon code must be unique!"),
    ]

    name = fields.Char(string="Name", required=True)
    description = fields.Text("Description")
    is_active = fields.Boolean(string="Is active?", default=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    partner_ids = fields.Many2many("res.partner", domain=[("active", "=", True)],
                                   string="List of Partners who can use this coupon")
    code = fields.Char(string="Coupon code", default=code_generate, required=True)
    is_counted = fields.Boolean(string="Is counted?", default=False)
    total = fields.Integer(string="Balance of coupons")
    coupon_type = fields.Selection(
        selection=[
            ("all", "All Products"),
            ("product", "For a single product"),
            ("category", "For a single category"),
        ], string="Is applicable: ", default="all"
    )
    product_id = fields.Many2one("product.product", string="Applicable product", domain=[("active", "=", True)])
    category_id = fields.Many2one("product.public.category", string="Applicable category")
    min_cart_value = fields.Integer(string="Minimum cart total")
    max_cart_value = fields.Integer(string="Maximum cart total")
    discount_type = fields.Selection([
        ('fixed', 'Fixed discount'),
        ('percentage', 'Percentage discount')
    ], string="Discount type", default='fixed', required=True)
    value = fields.Float(string="Discount value", default=1, required=True)

    @api.constrains('value')
    def _check_coupons_value(self):
        for r in self:
            if r.value < 0 or r.value == 0:
                raise ValidationError(_('Coupon value must be positive'))

    @api.constrains('total')
    def _check_coupons_total(self):
        for r in self:
            if r.total < 0:
                raise ValidationError(_('Number of coupons must be positive'))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for r in self:
            if r.start_date > r.end_date:
                raise ValidationError(_('"End date" must be later then "Start date"'))

    @api.constrains('min_cart_value', 'max_cart_value')
    def _check_cart(self):
        for r in self:
            if r.min_cart_value < 0:
                raise ValidationError(_('"Minimum cart total" must be positive'))
            if r.max_cart_value < 0:
                raise ValidationError(_('"Maximum cart total" must be positive'))
            if r.min_cart_value > r.max_cart_value:
                raise ValidationError(_('"Minimum cart total" must be later then "Maximum cart total"'))

    @api.constrains('code')
    def _check_coupone_code_length(self):
        for r in self:
            if len(r.code) < 4:
                raise ValidationError(_('Coupon code must have at least four characters'))
