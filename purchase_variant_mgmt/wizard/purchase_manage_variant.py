# -*- coding: utf-8 -*-
# © 2017 Comunitea Servicios Tecnológicos S.L. (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import odoo.addons.decimal_precision as dp
from openerp import models, api, fields

class PurchaseManageVariant(models.TransientModel):
    _name = 'purchase.manage.variant'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string="Template", required=True)
    variant_line_ids = fields.Many2many(
        comodel_name='purchase.manage.variant.line', string="Variant Lines")

    @api.multi
    def onchange(self, values, field_name, field_onchange):  # pragma: no cover
        if "variant_line_ids" in field_onchange:
            for sub in ("product_id", "disabled", "value_x", "value_y",
                        "product_qty", "y_order", "x_order"):
                field_onchange.setdefault("variant_line_ids." + sub, u"")
        return super(PurchaseManageVariant, self).onchange(
            values, field_name, field_onchange)

    @api.model
    def _get_order_str(self, values):
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
        if context['active_model'] == 'purchase.order.line':
            purchase_order = record.order_id
        else:
            purchase_order = record
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
                order_line = purchase_order.order_line.filtered(
                    lambda x: x.product_id == product)[:1]
                lines.append((0, 0, {
                    'product_id': product,
                    'disabled': not bool(product),
                    'value_x': value_x,
                    'value_y': value_y,
                    'product_qty': order_line.product_qty,
                    'x_order': x_order_str,
                    'y_order': y_order_str,
                }))
        self.variant_line_ids = lines

    @api.multi
    def button_transfer_to_order(self):
        context = self.env.context
        record = self.env[context['active_model']].browse(context['active_id'])
        if context['active_model'] == 'purchase.order.line':
            purchase_order = record.order_id
        else:
            purchase_order = record
        purchase_line = self.env['purchase.order.line']
        lines2unlink = purchase_line
        for line in self.variant_line_ids:
            order_line = purchase_order.order_line.filtered(
                lambda x: x.product_id == line.product_id)
            if order_line:
                if not line.product_qty:
                    # Done this way because there's a side effect removing here
                    lines2unlink |= order_line
                else:
                    order_line.product_qty = line.product_qty
            elif line.product_qty:
                order_line = purchase_line.new({
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_id,
                    'product_qty': line.product_qty,
                    'order_id': purchase_order.id,
                })
                order_line.onchange_product_id()
                order_line_vals = order_line._convert_to_write(
                    order_line._cache)
                order_line_vals['product_qty'] = line.product_qty
                purchase_order.order_line.create(order_line_vals)
        lines2unlink.unlink()


class PurchaseManageVariantLine(models.TransientModel):
    _name = 'purchase.manage.variant.line'

    product_id = fields.Many2one(
        comodel_name='product.product', string="Variant", readonly=True)
    disabled = fields.Boolean()
    value_x = fields.Many2one(comodel_name='product.attribute.value')
    value_y = fields.Many2one(comodel_name='product.attribute.value')
    product_qty = fields.Float(
        string="Quantity", digits=dp.get_precision('Product UoS'))
    x_order = fields.Char('X axis order')
    y_order = fields.Char('Y axis order')
