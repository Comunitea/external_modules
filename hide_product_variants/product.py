# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, api


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        if vals.get('image_variant', False):
            self.mapped('product_tmpl_id').write(
                {'image': vals['image_variant']})
        return super(ProductProduct, self).write(vals)
