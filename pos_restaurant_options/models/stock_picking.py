##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2022 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api
from odoo.tools import OrderedSet


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def _prepare_stock_move_vals(self, first_line, order_lines):
        res = super(StockPicking, self)._prepare_stock_move_vals(first_line, order_lines)
        if first_line.selected_attribute_value_ids and first_line.selected_attribute_value_ids != '[]':
            res.update({"selected_attribute_value_ids": first_line.selected_attribute_value_ids})
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    selected_attribute_value_ids = fields.Char('Attribute IDs')

    def action_explode(self):
        """ Explodes pickings """
        # Overwritten to add context to moves
        moves_ids_to_return = OrderedSet()
        moves_ids_to_unlink = OrderedSet()
        phantom_moves_vals_list = []
        ctx = self.env.context.copy()
        for move in self:
            ctx.update({
                'attribute_value_ids': move.selected_attribute_value_ids
            })
            if not move.picking_type_id or (move.production_id and move.production_id.product_id == move.product_id):
                moves_ids_to_return.add(move.id)
                continue
            bom = self.env['mrp.bom'].sudo()._bom_find(product=move.product_id, company_id=move.company_id.id, bom_type='phantom')
            if not bom:
                moves_ids_to_return.add(move.id)
                continue
            if move.picking_id.immediate_transfer:
                factor = move.product_uom._compute_quantity(move.quantity_done, bom.product_uom_id) / bom.product_qty
            else:
                factor = move.product_uom._compute_quantity(move.product_uom_qty, bom.product_uom_id) / bom.product_qty
            boms, lines = bom.with_context(ctx).sudo().explode(move.product_id, factor, picking_type=bom.picking_type_id)
            for bom_line, line_data in lines:
                if move.picking_id.immediate_transfer:
                    phantom_moves_vals_list += move._generate_move_phantom(bom_line, 0, line_data['qty'])
                else:
                    phantom_moves_vals_list += move._generate_move_phantom(bom_line, line_data['qty'], 0)
            # delete the move with original product which is not relevant anymore
            moves_ids_to_unlink.add(move.id)

        self.env['stock.move'].browse(moves_ids_to_unlink).sudo().unlink()
        if phantom_moves_vals_list:
            phantom_moves = self.env['stock.move'].create(phantom_moves_vals_list)
            phantom_moves._adjust_procure_method()
            moves_ids_to_return |= phantom_moves.action_explode().ids
        return self.env['stock.move'].browse(moves_ids_to_return)