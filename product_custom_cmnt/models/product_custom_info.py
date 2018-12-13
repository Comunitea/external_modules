# -*- coding: utf-8 -*-
# Copyright 2017 Kiko Sánchez <kiko@comunitea.com>

# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html


from odoo.osv import expression
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCustomOption(models.Model):

    _name = "product.custom.option"
    _order = "property_id, default_option desc, sequence"

    sequence = fields.Integer("Sequence", default=10)
    property_id = fields.Many2one('product.custom.property', string="Custom property", required=True)
    template_id = fields.Many2one(related='property_id.template_id', string="Custom template", store=True)
    name = fields.Char('Value', required=True, translate=True)
    default_option = fields.Boolean("Default option", default=False)

    _sql_constraints = [
        ('option_unique', 'unique(property_id, name)', 'Option value must be unique per property!'),
    ]


    @api.multi
    def write(self, vals):
        if vals.get('default_option', False):
            self.ensure_one()
            domain = [('property_id', '=', self.property_id.id), ('default_option', '=', True)]
            self.env["product.custom.option"].search(domain).write({'default_option': False})
        super(ProductCustomOption, self).write(vals)


    @api.model
    def create(self, vals):
        if vals['default_option']:
            domain = [('property_id', '=', vals['property_id']), ('default_option', '=', True)]
            self.env["product.custom.option"].search(domain).write({'default_option': False})

        res = super(ProductCustomOption, self).create(vals)

        if res.default_option:
            domain = [('product_custom_template_ids', 'in', res.template_id.id)]
            product_tmpl_ids = self.env['product.template'].search(domain)
            product_tmpl_ids.check_product_custom_value_ids(res)
        return res


    @api.multi
    def unlink(self):
        return super(ProductCustomOption, self).unlink()

class ProductInfoProperty(models.Model):

    _name = "product.custom.property"
    _description = "Model to add custom property in product"

    name = fields.Char("Name", required=True, translate=True)
    template_id = fields.Many2one("product.custom.template", string="Custom template values", required=True)
    sequence = fields.Integer("Sequence", default=10)
    option_ids = fields.One2many('product.custom.option', 'property_id')
    default_option_id = fields.Many2one('product.custom.option', 'Default option', compute="get_default_option")
    type = fields.Selection(selection=[('normal', 'Normal'),
                                       ('sport', 'Sport'),
                                       ('origin_country', 'Pais de Origen')], string='Property type', default='normal')

    _sql_constraints = [
        ('template_unique', 'unique(template_id, name)', 'Property must be unique per template!'),
    ]

    @api.multi
    def get_default_option(self):
        for property in self:
            property.default_option_id = property.option_ids.filtered(lambda x: x.default_option)


    @api.multi
    def unlink(self):
        for property in self:
            property.option_ids.unlink()
        return super(ProductInfoProperty, self).unlink()

class ProductInfoTemplate(models.Model):

    _name = "product.custom.template"
    _description = "Model to add custom template to product/template"

    @api.multi
    def get_option_ids(self):
        for template in self:
            domain = [('property_id', 'in', template.property_ids.ids)]
            template.option_ids = self.env['product.custom.option'].search(domain)

    name = fields.Char('name', required=True, translate=True)
    property_ids = fields.One2many('product.custom.property', 'template_id', string="Properties")
    option_ids = fields.One2many('product.custom.option', string="Values", compute=get_option_ids)






