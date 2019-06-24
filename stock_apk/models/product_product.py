# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductUom(models.Model):
    _inherit = "product.uom"


    @api.multi
    @api.depends('rounding')
    def _get_integer_rounding(self):
        for unit in self:
            scale = 0
            r = unit.rounding
            while r < 1:
                r = r * 10
                scale += 1
            unit.round_float = scale


    round_float = fields.Integer ('Integer rounding', compute='_get_integer_rounding', store=True)

    @api.model
    def get_apk_vals(self, type='normal'):
        vals = {'id': self.id,
                'name': self.name,
                'rounding': self.round_float}
        return vals

    @api.model
    def compute_qty_apk(self, values):
        from_unit = values.get('from_unit')
        to_unit = values.get('to_unit')
        qty = values.get('qty')
        from_unit_id = self.env['product_uom'].browse(from_unit)
        to_unit_id = self.env['product_uom'].browse(to_unit)
        return from_unit_id._compute_quantity(qty, to_unit_id)


class ProductTemplate(models.Model):

    _inherit = "product.template"

    short_name = fields.Char("Short name")
    need_qty_check = fields.Boolean()
    need_check = fields.Boolean("Barcode check required", default=False)


class ProductProduct(models.Model):

    _inherit = "product.product"

    product_tmpl_name = fields.Char(related='product_tmpl_id.name')
    tracking = fields.Selection(related='product_tmpl_id.tracking')

    @api.model
    def get_apk_vals(self, type='normal'):
        if not self:
            return False
        vals = {'id': self.id,
                'name': self.short_name or self.display_name
                }

        if type != 'min':
            vals.update({'barcode': self.barcode,
                         'default_code': self.default_code,
                         'tracking': self.tracking,
                         'qty_available': self.qty_available,
                         'need_qty_check': self.need_qty_check,
                         'product_tmpl_id': self.product_tmpl_id.id,
                         'uom_id': self.uom_id.get_apk_vals()})

        if type == 'form':
            vals.update({
                'image': self.image_small
            })
        print('Product: valores {} \n {}'.format(type, vals))
        return vals