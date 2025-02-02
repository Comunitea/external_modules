from odoo import models, fields, api, _
from itertools import groupby


class PosSession(models.Model):

    _inherit = "pos.session"
    
    def _loader_params_product_attribute_value(self):
        res = super()._loader_params_product_attribute_value()
        res["search_params"]["fields"].append("bom_product_id")
        return res
    
    
    def _get_attributes_by_ptal_id(self):
        product_attributes = self.env['product.attribute'].search([('create_variant', '=', 'no_variant')])
        product_template_attribute_values = self.env['product.template.attribute.value'].search([
            ('attribute_id', 'in', product_attributes.ids),
        ])
        product_template_attribute_values._read(['attribute_id', 'attribute_line_id', 'product_attribute_value_id', 'price_extra', 'ptav_active'])
        product_template_attribute_values.product_attribute_value_id._read(['name', 'is_custom', 'html_color'])

        def key1(ptav):
            return ptav.attribute_line_id.id, ptav.attribute_id.id

        def key2(ptav):
            return ptav.attribute_line_id.id, ptav.attribute_id
        res = {}
        for key, group in groupby(sorted(product_template_attribute_values, key=key1), key=key2):
            attribute_line_id, attribute = key
            values = [{'id': ptav.product_attribute_value_id.id,
                       'name': ptav.product_attribute_value_id.name,
                       'is_custom': ptav.is_custom,
                       'html_color': ptav.html_color,
                       'price_extra': ptav.price_extra,
                       'bom_product_id':[
                           ptav.product_attribute_value_id.bom_product_id.id, 
                           ptav.product_attribute_value_id.bom_product_id.name] if ptav.product_attribute_value_id.bom_product_id else False
                           } for ptav in list(group) if ptav.ptav_active]
            res[attribute_line_id] = {
                'id': attribute_line_id,
                'name': attribute.name,
                'display_type': attribute.display_type,
                'values': values,
            }

        return res