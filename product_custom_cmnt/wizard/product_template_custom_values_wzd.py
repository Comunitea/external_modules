# -*- coding: utf-8 -*-
# © 2016 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from odoo import models, fields, exceptions, api, _
from odoo.exceptions import ValidationError


class PtcwLine(models.TransientModel):

    _name = 'ptcw.line'

    wzd_id = fields.Many2one('product.template.custom.value.wzd', 'Wizard')
    template_id = fields.Many2one('product.custom.template', 'Template')
    property_id = fields.Many2one('product.custom.property', 'Property')#, domain="[('template_id', 'in', wzd_id.template_ids)]")
    option_id = fields.Many2one('product.custom.option', 'Option')#, domain="[('property_id', '=', property_id)]")
    new_line = fields.Boolean('New line', default=True, readonly=True)

    _sql_constraints = [
        ('value_unique', 'unique(wzd_id, property_id)', 'property/value must be unique per template!'),
    ]


class ProductTemplateCustomValueWzd(models.TransientModel):

    _name = 'product.template.custom.value.wzd'

    @api.multi
    @api.depends('line_ids.property_id')
    def get_property(self):
        self.ensure_one()
        self.custom_property_ids = [(6, 0, self.line_ids.mapped('property_id').ids)]

    product_template_id = fields.Many2one('product.template', string="Apply in this product templates")
    custom_template_ids = fields.Many2many('product.custom.template', string="Custom templates")
    custom_property_ids = fields.Many2many('product.custom.property', compute="get_property")
    line_ids = fields.One2many('ptcw.line', 'wzd_id', "Lines")


    @api.model
    def default_get(self, fields):
        return super(ProductTemplateCustomValueWzd, self).default_get(fields)

    @api.multi
    def name_get(self):
        result = []
        for value in self:
            name = "{}: {}".format((_('Value template')), value.custom_template_ids.mapped('name'))
            result.append((value.id, name))
        return result


    def refresh_product_template(self):
        self.product_template_id.write({'product_custom_option_ids': [(6, 0, self.line_ids.mapped('option_id').ids)]})
