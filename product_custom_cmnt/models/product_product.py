# -*- coding: utf-8 -*-
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, fields, models
from odoo.osv import expression

class ProductProduct(models.Model):

    _inherit = "product.product"

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):

        if 'custom_template_id' in self._context:
            my_arg = [['product_tmpl_id.product_custom_template_ids.name', u'=', self._context.get('custom_template_id')]]
            args = expression.AND([my_arg, args])
        if 'custom_property_id' in self._context:
            my_arg = [['product_tmpl_id.product_custom_option_ids.property_id.name', u'=', self._context.get('custom_property_id')]]
            args = expression.AND([my_arg, args])
        if 'custom_option_id' in self._context:
            my_arg = [['product_tmpl_id.product_custom_option_ids.name', u'=', self._context.get('custom_option_id')]]
            args = expression.AND([my_arg, args])

        return super(ProductProduct, self).search(args, offset=offset, limit=limit, order=order, count=count)

