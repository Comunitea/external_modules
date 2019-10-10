# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp


class ProductAlternativeVariantWzd(models.TransientModel):

    _name = 'product.alternative.variant.wzd'
    _description = 'alternative products wizard'

    wzd_id = fields.Many2one('product.alternative.wzd')
    name = fields.Char('Display name', readonly=True)
    product_id = fields.Many2one(
        'product.product', string="Product", readonly=True)
    uom_id = fields.Many2one('uom.uom', string='uom_id', readonly=True)
    selected = fields.Boolean('selected', default=False)

    default_code = fields.Char('Default code', readonly=True)
    lst_price = fields.Float(
        'Public Price', digits=dp.get_precision('Product Price'), readonly=True)
    image_small = fields.Binary("image_small", readonly=True)
    currency_id = fields.Many2one(
        'res.currency', 'Currency')
    qty_available = fields.Float(
        'Quantity On Hand',
        digits=dp.get_precision('Product Unit of Measure'))

    p_id = fields.Integer(related="product_id.id")


    @api.multi
    def set_as_selected(self):
        if self._context.get('new_product_id', False):
            ol = self.env['sale.order.line'].browse(
                self._context.get('default_sale_order_line_id'))
            product_uom_qty = ol.product_uom_qty
            ol.product_id = self._context.get('new_product_id')
            ol.product_id_change()
            ol.product_uom_qty = product_uom_qty
            ol.product_uom_change()


class ProductAlternativeWzd(models.TransientModel):

    _name = 'product.alternative.wzd'
    _description = 'alternative products wizard'

    sale_order_line_id = fields.Many2one(
        'sale.order.line', string='Sale order line')
    product_id = fields.Many2one(
        'product.product', string='Product')
    alternative_product_ids = fields.Many2many(
        'product.alternative.variant.wzd', string='Alternative product',
        readonly=True)
    default_code = fields.Char(
        related='product_id.default_code', readonly="1")
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')
    lst_price = fields.Float(
        'Public Price', digits=dp.get_precision('Product Price'),
        readonly=True)
    image_medium = fields.Binary(related='product_id.image_medium')
    qty_available = fields.Float(related='product_id.qty_available',
                                 readonly="1")
    virtual_available = fields.Float(
        related='product_id.virtual_available', readonly="1")
    p_id = fields.Integer("product_id")
    currency_id = fields.Many2one('res.currency', 'Currency')


    @api.model
    def get_values(self, product_id=False):
        if not product_id:
            return False
        line_id = self.env['sale.order.line'].browse(
            self._context.get('default_sale_order_line_id'))
        alternative_ids = product_id.alternative_product_ids.\
            mapped('product_variant_ids')
        return {'p_id': product_id.id,
                'product_id': product_id.id,
                'lst_price': line_id.price_unit,
                'sale_order_line_id':
                self._context.get('default_sale_order_line_id'),
                'alternative_product_ids': [
                    (0, 0, {'product_id': alternative.id,
                            'display_name': alternative.display_name,
                            'default_code': alternative.default_code,
                            'p_id': alternative.id,
                            'wzd_id': self.id,
                            'qty_available': alternative.qty_available,
                            'currency_id': line_id.currency_id.id,
                            'uom_id': alternative.uom_id.id,
                            'lst_price':
                            line_id.get_price_for_product(alternative)
                            }) for alternative in alternative_ids]
                }

    @api.model
    def default_get(self, fields):
        res = super(ProductAlternativeWzd, self).default_get(fields)
        product_id = self.env['product.product'].\
            browse(self._context.get('default_product_id'))
        res.update(self.get_values(product_id))
        print (res)
        return res

    @api.model
    def set_as_selected(self):
        return True

    def change_sale_order_line(self):
        return True

