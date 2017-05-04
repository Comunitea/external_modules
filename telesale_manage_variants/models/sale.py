# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api
# import time


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _get_ts_template_line_vals(self, order_obj, line):
        t_product = self.env['product.product']
        product_obj = t_product.browse(line['product_id'])
        product_uom_id = line.get('product_uom', False)
        product_uom_qty = line.get('qty', 0.0)
        vals = {
            'order_id': order_obj.id,
            'name': product_obj.name,
            'product_template': product_obj.product_tmpl_id.id,
            'product_id': product_obj.id,
            'price_unit': line.get('price_unit', 0.0),
            'product_uom': product_uom_id,
            'product_uom_qty': product_uom_qty,
            'tax_id': [(6, 0, line.get('tax_ids', False))],
            'discount': line.get('discount', 0.0),
        }
        return vals

    @api.model
    def _get_ts_parent_template_line_vals(self, order_obj, line, total_qty):
        t_product = self.env['product.product']
        product_obj = t_product.browse(line['product_id'])
        vals = {
            'order_id': order_obj.id,
            'product_template': product_obj.product_tmpl_id.id,
            'name': product_obj.product_tmpl_id.display_name,
            'product_uom': line.get('product_uom', False),
            'product_uom_qty': total_qty,
            'product_id': product_obj.product_tmpl_id.product_variant_ids[0].id
        }
        return vals

    @api.model
    def _create_lines_from_ui(self, order_obj, order_lines):
        """
        Overwrited to create template_lines
        """
        t_order_line = self.env['sale.order.line']
        t_template_line = self.env['sale.order.line.template']

        # grouping_lines = [] # list of cid of lines with more than one variant
        child_lines = {}     # Key is parent cid, value list of variant lines
        child_qty = {}     # Key is parent cid, value total qty lines

        # Create template_single lines and get structure to create grouping
        # lines and child.
        for line in order_lines:
            mode = line.pop('mode')
            line.pop('cid')

            if mode == 'template_single':
                vals = self._get_ts_template_line_vals(order_obj, line)
                t_template_line.create(vals)
            elif mode == 'template_variants':
                continue
            elif mode == 'variant':
                p_cid = line.pop('parent_cid')
                if p_cid not in child_lines:
                    child_lines[p_cid] = []
                child_lines[p_cid].append(line)

                if p_cid not in child_qty:
                    child_qty[p_cid] = 0.0
                child_qty[p_cid] += line.get('qty', 0.0)

        ctx = dict(self._context)
        ctx.update({'no_create_line': True})
        t_template_line2 = t_template_line.with_context(ctx)
        for p_cid in child_lines:
            #  Create parent line
            list_child_lines = child_lines[p_cid]
            line = list_child_lines[0]
            qty = child_qty[p_cid]
            vals = self._get_ts_parent_template_line_vals(order_obj, line, qty)
            template_line_obj = t_template_line2.create(vals)

            #  Create child lines
            for child_line in list_child_lines:
                vals = self._get_ts_line_vals(order_obj, child_line)
                vals.update({'template_line': template_line_obj.id})
                t_order_line.create(vals)
