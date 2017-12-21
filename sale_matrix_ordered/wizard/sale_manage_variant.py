# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.addons.decimal_precision as dp
from odoo import api, models, fields


class SaleManageVariant(models.TransientModel):
    _inherit = 'sale.manage.variant'

    # FULL OVERWRITE
    # ADD X Y ORDER FIELDS
    @api.multi
    def onchange(self, values, field_name, field_onchange):  # pragma: no cover
        if "variant_line_ids" in field_onchange:
            for sub in ("product_id", "disabled", "value_x", "value_y",
                        "product_uom_qty", "y_order", "x_order"):
                field_onchange.setdefault("variant_line_ids." + sub, u"")
        return super(SaleManageVariant, self).onchange(
            values, field_name, field_onchange)

    def _get_order_str(self, values):
        """
        Get the ids ordered into a string separated by ,. EX "29,32,3031"
        The matrix widget will interpretate that order.
        """
        res = ""
        if values:
            str_ids = map(str, values.ids)   # already_ordered
            res = ','.join(str_ids)
        return res

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id(self):
        self.variant_line_ids = [(6, 0, [])]
        template = self.product_tmpl_id
        context = self.env.context
        record = self.env[context['active_model']].browse(
            context['active_id'])
        if context['active_model'] == 'sale.order.line':
            sale_order = record.order_id
        else:
            sale_order = record
        num_attrs = len(template.attribute_line_ids)
        if not template or not num_attrs:
            return
        line_x = template.attribute_line_ids[0]
        line_y = False if num_attrs == 1 else template.attribute_line_ids[1]
        lines = []

        x_order_str = self._get_order_str(line_x.value_ids)
        y_order_str = \
            self._get_order_str(line_y and line_y.value_ids or [False])

        for value_x in line_x.value_ids:
            for value_y in line_y and line_y.value_ids or [False]:
                # Filter the corresponding product for that values
                values = value_x
                if value_y:
                    values += value_y
                product = template.product_variant_ids.filtered(
                    lambda x: not(values - x.attribute_value_ids))[:1]
                order_line = sale_order.order_line.filtered(
                    lambda x: x.product_id == product)[:1]
                lines.append((0, 0, {
                    'product_id': product,
                    'disabled': not bool(product),
                    'value_x': value_x,
                    'value_y': value_y,
                    'product_uom_qty': order_line.product_uom_qty,
                    'x_order': x_order_str,
                    'y_order': y_order_str,
                }))
        self.variant_line_ids = lines


class SaleManageVariantLine(models.TransientModel):
    _inherit = 'sale.manage.variant.line'

    # Adding ordered fields in order to read it in the javascript widget
    x_order = fields.Char('X axis order')
    y_order = fields.Char('Y axis order')

