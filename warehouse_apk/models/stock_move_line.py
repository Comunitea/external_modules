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

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    tracking = fields.Selection(related='move_id.tracking')

    @api.model
    def force_set_qty_done_apk(self, vals):
        move = self.browse(vals.get('id', False))
        field = vals.get('field', False)
        if not move:
            return {'err': True, 'error': "No se ha encontrado el movimiento."}
        move.qty_done = move.product_uom_qty
        return True

    @api.model
    def find_move_line_id(self, vals):

        picking_id = vals.get('picking_id')
        code = vals.get('search_str')
        domain_base = [('picking_id', '=', picking_id)]
        domain = domain_base + [('lot_id.name', '=', code)]
        res = self.search_read(domain, ['id'], limit=1)
        if res:
            print ("Encuentro lote")
            return res[0]['id']
        domain = domain_base + [('product_id.barcode', '=', code)]
        res = self.search_read(domain, ['id'], limit=1)
        if res:
            print("Encuentro barcode")
            return res[0]['id']

        domain = domain_base + [('product_id.default_code', '=', code)]
        res = self.search_read(domain, ['id'], limit=1)
        if res:
            print("Encuentro ref")
            return res[0]['id']
            return self.get_move_line_info_apk({'move_id': res[0]['id']})
        return False

    @api.model
    def force_set_qty_done_by_product_code_apk(self, vals):

        default_code = vals.get('default_code', False)
        picking = vals.get('picking', False)
        product = self.env['product.product'].search([('default_code', '=', default_code)])
        if not product:
            return {'err': True, 'error': "No se ha encontrado ese default_code en ningún producto."}
        _logger.info("Encontrado el producto {} con default_code: {}.".format(product.name, default_code))
        move_line = self.search([('product_id', '=', product.id), ('picking_id', '=', int(picking))])
        _logger.info("Encontrada move line {} con product_id: {} del picking {}.".format(move_line, product.id, picking))
        move_line = self.browse(move_line.id)
        
        field = vals.get('field', False)
        if not move_line:
            return {'err': True, 'error': "No se ha encontrado ninguna línea en la que aparezca ese producto."}
        ctx = self._context.copy()
        ctx.update(model_dest="stock.move.line")
        ctx.update(field=field)
        res = move_line.with_context(ctx).force_set_qty_done() 
        return True

    ## APK
    @api.model
    def get_move_line_info_apk(self, vals):
        move_id = vals.get('id', False)
        index = vals.get('index', 0)
        if index:
            picking_id = self.search_read([('id', '=', move_id)], ['picking_id'])
            if not picking_id:
                return False

        if not move_id:
            return False
        move_line = self.browse(move_id)
        move_line_ids = move_line.picking_id.move_line_ids
        if index != 0:
            if index == -1:
                move_line_ids = reversed(move_line_ids)
            is_index = False
            for new_move in move_line_ids:
                if is_index:
                    break
                is_index = new_move == move_line
            if is_index:
                move_line = new_move
        product_id = move_line.move_id.product_id.with_context(location=move_line.move_id.location_id.id)
        data = {'id': move_line.id,
                'name': product_id.display_name,
                'image': product_id.image_medium,
                'barcode': product_id.barcode,
                'tracking': product_id.tracking,
                'default_code': product_id.default_code,
                'qty_available': product_id.qty_available,
                'location_id': {'id': move_line.location_id.id,
                                'name': move_line.location_id.name,
                                'barcode': move_line.location_id.barcode},
                'location_dest_id': {'id': move_line.location_dest_id.id,
                                     'name': move_line.location_dest_id.name,
                                     'barcode': move_line.location_dest_id.barcode},
                'product_uom_qty': move_line.product_uom_qty,
                'uom_move': {'uom_id': move_line.product_uom_id.id, 'name': move_line.product_uom_id.name},
                'qty_done': move_line.qty_done,
                'lot_id': {'id': move_line.lot_id and move_line.lot_id.id or False,
                           'name': move_line.lot_id and move_line.lot_id.name or ''}
                }
        print(data)
        return data