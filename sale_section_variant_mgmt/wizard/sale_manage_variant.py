# © 2019 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models, fields


class SaleManageVariant(models.TransientModel):
    _inherit = 'sale.manage.variant'
    
    @api.model
    def _default_layout(self):
        context = self.env.context
        # Obtengo la sección desde la línea desde la que se abre el asistente
        layout_category_id = False
        if context['active_model'] == 'sale.order.line':
            record = self.env[context['active_model']].\
                browse(context['active_id'])
            layout_category_id = record.layout_category_id
        return layout_category_id

    layout_category_id = fields.Many2one(
        'sale.layout_category', 'Section', default=_default_layout)

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id(self):
        """
        Overwrited to load onnly order lines whitch match the section
        """
        self.variant_line_ids = [(6, 0, [])]
        template = self.product_tmpl_id
        context = self.env.context
        record = self.env[context['active_model']].browse(
            context['active_id'])
        
        # Obtengo la sección cargada por defecto desde la línea o vacía
        layout_category_id = self.layout_category_id
        if context['active_model'] == 'sale.order.line':
            sale_order = record.order_id
        else:
            sale_order = record
        attr_lines = template.attribute_line_ids.filtered(
            lambda x: x.attribute_id.create_variant
        )
        num_attrs = len(attr_lines)
        if not template or not num_attrs or num_attrs > 2:
            return
        line_x = attr_lines[0]
        line_y = False if num_attrs == 1 else attr_lines[1]
        lines = []
        for value_x in line_x.value_ids:
            for value_y in line_y and line_y.value_ids or [False]:
                product = self._get_product_variant(value_x, value_y)
                if not product:
                    continue

                # Buscar línea por sección
                order_line = sale_order.order_line.filtered(
                lambda x: x.product_id == product and
                x.layout_category_id == layout_category_id)[:1]

                lines.append((0, 0, {
                    'value_x': value_x,
                    'value_y': value_y,
                    'product_uom_qty': order_line.product_uom_qty,
                }))
        self.variant_line_ids = lines
    
    @api.multi
    def button_transfer_to_order(self):
        """
        Overwrited to add the section
        """
        context = self.env.context
        record = self.env[context['active_model']].browse(context['active_id'])
        if context['active_model'] == 'sale.order.line':
            sale_order = record.order_id
        else:
            sale_order = record
        OrderLine = self.env['sale.order.line']
        lines2unlink = OrderLine
        for line in self.variant_line_ids:
            product = self._get_product_variant(line.value_x, line.value_y)
            # Filtrar por sección
            order_line = sale_order.order_line.filtered(
                lambda x: x.product_id == product and
                x.layout_category_id == self.layout_category_id
            )
            if order_line:
                if not line.product_uom_qty:
                    # Done this way because there's a side effect removing here
                    lines2unlink |= order_line
                else:
                    order_line.product_uom_qty = line.product_uom_qty
            elif line.product_uom_qty:
                vals = OrderLine.default_get(OrderLine._fields.keys())
                vals.update({
                    'product_id': product.id,
                    'product_uom': product.uom_id,
                    'product_uom_qty': line.product_uom_qty,
                    'order_id': sale_order.id,
                    'layout_category_id': self.layout_category_id.id
                })
                order_line = OrderLine.new(vals)
                order_line.product_id_change()
                order_line_vals = order_line._convert_to_write(
                    order_line._cache)
                sale_order.order_line.browse().create(order_line_vals)
        lines2unlink.unlink()
    
    
    @api.onchange('layout_category_id')
    def _onchange_layout_category_id(self):
        self._onchange_product_tmpl_id()