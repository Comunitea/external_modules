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

    ## APK

    @api.model
    def force_set_qty_done_apk(self, vals):
        move = self.browse(vals.get('id', False))
        field = vals.get('field', False)
        if not move:
            return {'err': True, 'error': "No se ha encontrado el movimiento."}
        ctx = self._context.copy()
        ctx.update(model_dest="stock.move.line")
        ctx.update(field=field)
        res = move.with_context(ctx).force_set_qty_done() 
        return True

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