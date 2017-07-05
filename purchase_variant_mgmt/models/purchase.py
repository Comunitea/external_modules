# -*- coding: utf-8 -*-
# © 2017 Comunitea Servicios Tecnológicos S.L. (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # This field is for avoiding conflicts with other module, that
    # adds product_tmpl_id, and its possible modifications. This field name
    # for sure won't conflict
    product_tmpl_id_purchase_order_variant_mgmt = fields.Many2one(
        comodel_name="product.template", related="product_id.product_tmpl_id",
        readonly=True)
    product_attribute_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        related="product_id.attribute_value_ids",
        readonly=True)
