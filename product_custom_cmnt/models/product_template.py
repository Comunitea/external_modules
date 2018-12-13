# -*- coding: utf-8 -*-
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import _, api, fields, models
from odoo.osv import expression



class ProductTemplate(models.Model):

    _inherit = "product.template"

    product_custom_template_id = fields.Many2one('product.custom.template', 'Main custom template')
    product_custom_template_ids = fields.Many2many('product.custom.template', 'product_template_custom_template_rel', 'product_tmpl_id', 'template_id', string="Custom template(s)")
    product_custom_option_ids = fields.Many2many('product.custom.option', 'product_template_custom_option_rel', 'product_tmpl_id', 'option_id', string ="Custom options")

    product_custom_property_id = fields.Many2one(
        'product.custom.property', 'Custom Property', store=False,
        help='Technical field. Used for searching on custom property, not stored in database.')
    product_custom_option_id = fields.Many2one(
        'product.custom.option', 'Custom option', store=False,
        help='Technical field. Used for searching on custom options, not stored in database.')

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):

        if 'custom_template_id' in self._context:
            my_arg = [['product_custom_template_ids.name', u'=', self._context.get('custom_template_id')]]
            args = expression.AND([my_arg, args])

        if 'custom_property_id' in self._context:
            my_arg = [['product_custom_option_ids.property_id.name', u'=', self._context.get('custom_property_id')]]
            args = expression.AND([my_arg, args])

        if 'custom_option_id' in self._context:
            my_arg = [['product_custom_option_ids.name', u'=', self._context.get('custom_option_id')]]
            args = expression.AND([my_arg, args])

        return super(ProductTemplate, self).search(args, offset=offset, limit=limit, order=order, count=count)


    @api.multi
    def check_product_custom_value_ids(self, pcv_id):
        tmpl_to_add = self.filtered(
            lambda x: not x.product_custom_option_ids.filtered(lambda y: y.property_id == pcv_id.property_id))
        tmpl_to_add.write({'product_custom_option_ids': [(4, pcv_id.id)]})
        return True

    @api.multi
    def refresh_template_custom_option(self):
        for p_tmpl in self:
            for property in p_tmpl.product_custom_template_ids.property_ids:
                values_to_check = p_tmpl.product_custom_option_ids.filtered(lambda x: x.property_id.id == property.id)
                # compruebo si hay más de uno y borro lo que no esté por defecto
                if len(values_to_check) > 1:
                    for x in values_to_check.filtered(lambda x: not x.default_option):
                        p_tmpl.write({'product_custom_option_ids': [(3, x.id)]})
                    values_to_check = p_tmpl.product_custom_option_ids.filtered(
                        lambda x: x.property_id.id == property.id)

                # Si está vacío y la property tiene force create, entonces la creo con el valor por defecto
                if not values_to_check and property.default_option_id:
                    p_tmpl.write({'product_custom_option_ids': [(4, property.default_option_id.id)]})

    @api.multi
    def get_custom_values_wzd(self):

        self.ensure_one()
        #import ipdb; ipdb.set_trace()
        product_template_properties = self.product_custom_option_ids.mapped('property_id')
        custom_template_property = self.product_custom_template_ids.mapped('property_ids')
        line_values = []

        for option in self.product_custom_option_ids:
            line_values.append({
                   'template_id': option.property_id.template_id.id,
                   'property_id': option.property_id.id,
                   'option_id': option.id,
                   'new_line': False})

        for property in custom_template_property - product_template_properties:
            if property.default_option_id:
                line_values.append({
                    'template_id': property.template_id.id,
                    'property_id': property.id,
                    'option_id': property.default_option_id.id,
                    'new_line': True})

        vals = {'product_template_id': self.id,
                'custom_template_ids': [(6, False, self.product_custom_template_ids.ids)],
                'line_ids': [(0, 0, x) for x in line_values]}
        obj = self.env['product.template.custom.value.wzd'].create(vals)
        return {
            'name': _('Product custom values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.template.custom.value.wzd',
            'target': 'new',
            'res_id': obj.id
        }

