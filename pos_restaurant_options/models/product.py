import json
from odoo import models, fields, api, _


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    combination_max_qty = fields.Integer('Combination quantity')

    def write(self, vals):
        res = super().write(vals)
        if vals.get("attribute_line_ids"):
            for value in self.attribute_line_ids.value_ids:
                value._create_bom_lines_product_id(template_id=self)
        if vals.get("combination_max_qty"):
            if self.used_in_bom_count and self.used_in_bom_count > 0:
                bom_lines = self.env['mrp.bom.line'].search(
                    [('product_tmpl_id', '=', self.id)]
                )
                for line in bom_lines:
                    line.product_qty = 1/self.combination_max_qty
        return res


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    bom_product_id = fields.Many2one('product.product', string='Product')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if vals.get("bom_product_id"):
            res._create_bom_lines_product_id()
        return res

    def write(self, vals):
        res = super().write(vals)
        if vals.get("bom_product_id"):
            self._create_bom_lines_product_id()
        return res

    def _create_bom_lines_product_id(self, template_id=False):
        for value in self:
            templates = template_id if template_id else value.attribute_id.product_tmpl_ids
            for template in templates:
                if template.bom_ids:
                    for bom in template.bom_ids:
                        product_template_attribute_id = self.env['product.template.attribute.value'].search([
                            ('product_attribute_value_id', '=', value.id)
                        ], limit=1)
                        if product_template_attribute_id and product_template_attribute_id not in bom.bom_line_ids.bom_product_template_attribute_value_ids:
                            values = {
                                'product_id': value.bom_product_id.id,
                                'product_qty': 1/(value.bom_product_id.combination_max_qty or 1),
                                'bom_product_template_attribute_value_ids': [(6, 0, product_template_attribute_id.ids)],
                                'bom_id': bom.id,
                            }
                            self.env['mrp.bom.line'].create(values)
