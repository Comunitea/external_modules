# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    def _compute_virtual_stock_conservative(self):
        for product in self:
            product.virtual_stock_conservative = product.qty_available - \
                product.outgoing_qty

    virtual_stock_conservative = fields.Float(
        compute="_compute_virtual_stock_conservative",
        readonly=True)


class ProductProduct(models.Model):

    _inherit = "product.product"

    def _compute_virtual_stock_conservative(self):
        for product in self:
            product.virtual_stock_conservative = product.qty_available - \
                product.outgoing_qty

    virtual_stock_conservative = fields.Float(
        compute="_compute_virtual_stock_conservative",
        readonly=True)
