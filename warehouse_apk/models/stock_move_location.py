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

from odoo import api, fields, models
from odoo.fields import first
import logging

_logger = logging.getLogger(__name__)

class StockMoveLocationWizard(models.TransientModel):
    _inherit = "wiz.stock.move.location"

    @api.model
    def create_wiz_from_apk(self, vals):
        location_barcode = vals.get('location_barcode', False)
        if location_barcode:
            location_id = self.env['stock.location'].search([('barcode', '=', location_barcode)], limit=1)
            if len(location_id) == 0:
                _logger.error("No se han encontrado ubicaciones con el barcode: {}".format(location_barcode))
                return {'err': True, 'error': "No se ha encontrado la ubicación."}
            _logger.info("Ubicaciones encontradas: {}".format(location_id))
        else:
            _logger.error("No se han encontrado ubicaciones con el barcode: {}".format(location_barcode))
            return {'err': True, 'error': "No se ha encontrado la ubicación."}
        
        wiz_move = self.create({
            'origin_location_id': location_id[0].id,
            'destination_location_id': 12
        })

        if wiz_move:
            _logger.info("Creado stock_move_location: {}".format(wiz_move))
            data = wiz_move._get_move_data()           
            return data
        else:
            _logger.error("No se ha podido crear el stock_move_location.")
            return {'err': True, 'error': "No se ha podido crear el movimiento."}
    
    @api.model
    def _get_move_data(self):
        for move in self:
            return {
                'id': move.id,
                'origin_location_id': {
                    'id': move.origin_location_id.id,
                    'name': move.origin_location_id.display_name
                },
                'destination_location_id': {
                    'id': move.destination_location_id.id,
                    'name': move.destination_location_id.display_name
                },
                'stock_move_location_line_ids': move._get_stock_move_location_line_ids()
            }
    
    @api.model
    def _get_stock_move_location_line_ids(self):
        location_lines = []
        for move in self.stock_move_location_line_ids:
            move_data = move._get_stock_move_location_line()
            location_lines.append(move_data)
        return location_lines

    @api.model
    def edit_wiz_location_from_apk(self, vals):
        move_id = vals.get('id', False)
        if move_id:
            move_id = self.browse(move_id)
        else:
            _logger.error("No se ha encontrado el movimiento")
            return {'err': True, 'error': "No se ha podido encontrar el movimiento."}
        origin_location_id = vals.get('origin_location_id', False)
        if origin_location_id:
            origin_location_id = self.env['stock.location'].search([('barcode', '=', origin_location_id)], limit=1)
            move_id.update({
                'origin_location_id': origin_location_id.id
            })
            for move_line in move_id.stock_move_location_line_ids:
                move_line.update({
                    'origin_location_id': origin_location_id.id
                })
        destination_location_id = vals.get('destination_location_id', False)
        if destination_location_id:
            destination_location_id = self.env['stock.location'].search([('barcode', '=', destination_location_id)], limit=1)
            move_id.update({
                'destination_location_id': destination_location_id.id
            })    
            for move_line in move_id.stock_move_location_line_ids:
                move_line.update({
                    'destination_location_id': destination_location_id.id
                })

        data = move_id._get_move_data()           
        
        return data

    @api.model
    def set_multiple_move_location(self, vals):       
        move_id = vals.get('id', False)
        action = vals.get('action', False)
        if move_id:
            move_id = self.browse(move_id)
        else:
            _logger.error("No se ha encontrado el movimiento")
            return {'err': True, 'error': "No se ha podido encontrar el movimiento."}

        try:
            for move in move_id.stock_move_location_line_ids:
                if action == 'set':
                    move.update({
                        'move_quantity': move.max_quantity
                    })
                elif action == 'reset':
                    move.update({
                        'move_quantity': 0
                    })
                else:
                    _logger.error("No se ha especificado una acción para modificar la cantidad.")
                    return {'err': True, 'error': "No se ha especificado una acción para modificar la cantidad."}
            return move_id._get_move_data()
        except Exception as e:
                _logger.error("No se ha podido editar el stock_move_location_line: {}".format(e))
                return {'err': True, 'error': "No se ha podido editar el movimiento: {}".format(e)}

    @api.model
    def action_move_location_apk(self, vals):
        move_id = vals.get('id', False)
        if move_id:
            move_id = self.browse(move_id)
        else:
            _logger.error("No se ha encontrado el movimiento")
            return {'err': True, 'error': "No se ha podido encontrar el movimiento."}
        try:
            res = move_id.action_move_location()
        except Exception as e:
            _logger.error("No se ha podido confirmar el movimiento: {}".format(e))
            return {'err': True, 'error': "No se ha podido confirmar el movimiento: {}".format(e)}
        
        return res.get('res_id', False)


class StockMoveLocationWizardLine(models.TransientModel):
    _inherit = "wiz.stock.move.location.line"

    @api.model
    def create_wiz_line_from_apk(self, vals):
        origin_location_id = vals.get('origin_location_id', False)
        product_barcode = vals.get('product_barcode', False)
        move_location_wizard_id = vals.get('move_location_wizard_id', False)
        destination_location_id = vals.get('destination_location_id', 12)

        if product_barcode:
            product_id = self.env['product.product'].search([('barcode', '=', product_barcode)], limit=1)
            _logger.info("Ubicaciones encontradas: {}".format(product_id))
        else:
            _logger.error("No se han encontrado productos productos con el barcode {} en la ubicación seleccionada".format(product_barcode))
            return {'err': True, 'error': "No se ha podido encontrar el producto."}
        
        search_args = [
            ('location_id', '=', origin_location_id),
            ('product_id', '=', product_id[0].id),
        ]
        res = self.env['stock.quant'].read_group(search_args, ['quantity'], [])
        max_quantity = res[0]['quantity']

        if max_quantity == None or max_quantity <= 0:
            _logger.error("No hay cantidades disponibles para este producto.")
            return {'err': True, 'error': "No hay cantidades disponibles para este producto."}

        move_line = self.create({
            'origin_location_id': origin_location_id,
            'product_id': product_id[0].id,
            'product_uom_id': product_id[0].product_tmpl_id.uom_id.id,
            'move_location_wizard_id': move_location_wizard_id,
            'destination_location_id': destination_location_id,
            'max_quantity': max_quantity
        })

        if move_line:
            _logger.info("Creado stock_move_location: {}".format(move_line))
            data = move_line[0]._get_stock_move_location_line()
            return data
        else:
            _logger.error("No se ha podido crear el stock_move_location_line.")
            return {'err': True, 'error': "No se ha podido crear el movimiento."}
    
    @api.model
    def _get_stock_move_location_line(self):

        data = {
            'id': self.id,
            'product_id': {
                'id': self.product_id.id,
                'name': self.product_id.display_name
            },
            'move_quantity': self.move_quantity,
            'max_quantity': self.max_quantity,
            'origin_location_id': {
                'id': self.origin_location_id.id,
                'name': self.origin_location_id.display_name
            },
            'destination_location_id': {
                'id': self.destination_location_id.id,
                'name': self.destination_location_id.display_name
            }
        }

        return data

    @api.model
    def edit_wiz_line_qty_from_apk(self, vals):
        move_id = vals.get('id', False)
        move_quantity = vals.get('move_quantity', False)
        if move_id:
            try:
                self.browse(move_id).update({
                    'move_quantity': move_quantity
                })
                return self.browse(move_id).move_location_wizard_id._get_move_data()
            except Exception as e:
                _logger.error("No se ha podido editar el stock_move_location_line: {}".format(e))
                return {'err': True, 'error': "No se ha podido editar el movimiento: {}".format(e)}
        else:
            _logger.error("No se ha podido encontrar el stock_move_location_line.")
            return {'err': True, 'error': "No se ha podido encontrar el movimiento."}