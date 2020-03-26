# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2019 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
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

from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ['stock.move', 'info.apk']

    tracking = fields.Selection(related='product_id.tracking')

    @api.model
    def force_set_qty_done_apk(self, vals):
        move = self.browse(vals.get('id', False))
        if not move:
            return {'err': True, 'error': "No se ha encontrado el movimiento."}
        for move_line in move.move_line_ids:
            move_line.qty_done = move_line.product_uom_qty
        return True

    @api.model
    def set_lot_ids_apk(self, vals):
        move_id = vals.get('id', False)
        reading = vals.get('reading', False)
        if not move_id or not reading:
            return False
        move = self.browse(move_id)
        move._do_unreserve()
        move_vals = {'product_id': move.product_id.id,
                     'picking_id': move.picking_id.id,
                     'move_id': move.id,
                     'location_id': move.location_id.id,
                     'location_dest_id': move.location_dest_id.id,
                     'product_uom_qty': 0,
                     'product_uom_id': move.product_uom.id}
        for line in reading:
            if '[' in line[0]:
                line[0] = line[0].replace('[', '')
                line[0] = line[0].replace(']', '')
                codes = line[0].split(',')
                for code in codes:
                    self.env['stock.move.line'].create(move_vals).write({'lot_name': code, 'qty_done': line[1]})
            else:
                self.env['stock.move.line'].create(move_vals).write({'lot_name': line[0], 'qty_done': line[1]})
        return True

    @api.model
    def set_qty_done_from_apk(self, vals):
        move_id = vals.get('id', False)
        quantity_done = vals.get('quantity_done', False)
        if not move_id or not quantity_done:
            return {'err': True, 'error': "No se ha enviado la línea o la cantidad a modificar."}
        move = self.browse(move_id)
        if not move:
            return {'err': True, 'error': "La línea introducida no existe."}
        try:
            move.update({
                'quantity_done': quantity_done
            })
            return True
        except Exception as e:
            return {'err': True, 'error': e}

    @api.model
    def get_move_info_apk(self, vals):
        move_id = vals.get('id', False)
        index = vals.get('index', 0)
        if index:
            picking_id = self.search_read([('id', '=', move_id)], ['picking_id'])
            if not picking_id:
                return False

        if not move_id:
            return False
        move = self.browse(move_id)
        move_lines = move.picking_id.move_lines
        if index != 0:
            if index == -1:
                move_lines = reversed(move_lines)
            is_index = False
            for new_move in move_lines:
                if is_index:
                    break
                is_index = new_move == move
            if is_index:
                move = new_move
        product_id = move.product_id.with_context(location=move.location_id.id)
        data = {'id': move.id,
                'display_name': product_id.display_name,
                'state': move.state,
                'image': product_id.image_medium,
                'barcode': product_id.barcode,
                'picking_id': {'id': move.picking_id.id,
                                'display_name': move.picking_id.display_name,
                                'code': move.picking_id.picking_type_code},
                'tracking': product_id.tracking,
                'default_code': product_id.default_code,
                'qty_available': product_id.qty_available,
                'location_id': {'id': move.location_id.id,
                                'display_name': move.location_id.display_name,
                                'barcode': move.location_id.barcode},
                'location_dest_id': {'id': move.location_dest_id.id,
                                     'display_name': move.location_dest_id.display_name,
                                     'barcode': move.location_dest_id.barcode},
                'product_uom_qty': move.product_uom_qty,
                'uom_move': {'uom_id': move.product_uom.id, 'name': move.product_uom.name},
                'quantity_done': move.quantity_done,
                'ready_to_validate': sum(line.qty_done for line in move.picking_id.move_line_ids) == sum(line.product_uom_qty for line in move.picking_id.move_line_ids)
                }
        lot_id = []
        lot_ids = move.move_line_ids.mapped("lot_id")
        lot_names = move.move_line_ids.mapped("lot_name")
        for lot in lot_ids:
            lot_id.append({
                'id': lot.id,
                'name': lot.name
            })
        for lot_name in lot_names:
            lot_id.append({
                'id': False,
                'name': lot_name
            })
        data['lot_ids'] = lot_id
        return data