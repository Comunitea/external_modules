from odoo import models, fields, api
import json


class MrpBom(models.Model):


    _inherit = 'mrp.bom'

    with_no_variant_attributes = fields.Boolean(string='With no variant attributes')

    @api.depends(
        'product_tmpl_id.attribute_line_ids.value_ids',
        'product_tmpl_id.attribute_line_ids.attribute_id.create_variant',
        'product_tmpl_id.attribute_line_ids.product_template_value_ids.ptav_active',
    )
    def _compute_possible_product_template_attribute_value_ids(self):
        for bom in self:
            if bom.with_no_variant_attributes:
                bom.possible_product_template_attribute_value_ids = bom.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids._only_active()
            else:
                super(MrpBom, bom)._compute_possible_product_template_attribute_value_ids()

    
class MrpBomLine(models.Model):

    _inherit = 'mrp.bom.line'

    def _skip_bom_line(self, product):
        self.ensure_one()
        attribute_value_ids = False
        list_attribute_value_ids = self.env.context.get("attribute_value_ids", [])
        if type(list_attribute_value_ids) is str:
            list_attribute_value_ids = json.loads(list_attribute_value_ids)
        if list_attribute_value_ids and len(list_attribute_value_ids) > 0:
            attribute_value_ids = self.env['product.attribute.value'].browse(list_attribute_value_ids)

        if self.bom_id and self.bom_id.with_no_variant_attributes:
            if attribute_value_ids and self.bom_product_template_attribute_value_ids.product_attribute_value_id in attribute_value_ids:
                return False
            return True
        else:
            return super(MrpBomLine, self)._skip_bom_line(product)