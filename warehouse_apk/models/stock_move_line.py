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
from odoo.tools import float_is_zero, float_compare
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

BINARYPOSITION = {'product_id': 0, 'location_id': 1, 'lot_id': 2, 'package_id': 3, 'location_dest_id': 4, 'result_package_id': 5, 'qty_done': 6}
FLAG_PROP = {'view': 1, 'req': 2, 'done': 4};

class StockMoveLine(models.Model):
    _inherit = ['info.apk', 'stock.move.line']
    _name = 'stock.move.line'

    tracking = fields.Selection(related='move_id.tracking')
    picking_type_id = fields.Many2one(related='move_id.picking_type_id')
    field_status_apk = fields.Char('000000',
                                         help="Indica el estado binario de los campos en la PDA:\n"
                                              "Product, Origen, Lote, Paquete, Destino, Paquete Destino y Cantidad\n"
                                              "Con los valores\n "
                                              "Bit 1 - Visible\nBit 2 - Requerido\nBit 3 - Hecho\n"
                                              "Validable cuando bit 3 está a 0")
    field_status = fields.Boolean('Ready', compute="compute_field_status", store=True)
    removal_priority = fields.Integer(compute='compute_move_order', store=True)


    @api.multi
    @api.depends('location_id', 'location_dest_id')
    def compute_move_order(self):
        for move in self:
            field = move.move_id.default_location
            move.removal_priority = move[field].removal_priority

    @api.depends('field_status_apk')
    def compute_field_status(self):
        for sml in self:
            sml.field_status = all(sml.read_status(field, 'done') or not sml.read_status(field, 'req') for field in BINARYPOSITION)

    def _read_status(self, field_status_apk, campo, propiedad):
        pos = BINARYPOSITION[campo]
        field = int(field_status_apk[pos:pos+1])
        return field & FLAG_PROP[propiedad] != 0

    def read_status(self, campo, propiedad):
        return self.field_status_apk and self._read_status(self.field_status_apk, campo=campo, propiedad=propiedad)

    @api.multi
    def write_status(self, campo, propiedad, value=True):
        for sml in self:
            field_status_apk = sml.field_status_apk
            field_status_apk = self._write_status(field_status_apk, campo=campo, propiedad=propiedad, value=value)
            val = {'field_status_apk': field_status_apk}
            if campo == 'lot_id' and propiedad == 'done':
                if value:
                    val.update(qty_done=sml.product_uom_qty)
                else:
                    val.update(qty_done=0)
                if sml.move_id.tracking != 'none':
                    field_status_apk = self._write_status(field_status_apk, campo='qty_done', propiedad='done',
                                                          value=value)
                    val.update(field_status_apk=field_status_apk)
            sml.write(val)

    def _write_status(self, field_status_apk, campo, propiedad, value=True):
        pos = BINARYPOSITION[campo]
        field = int(field_status_apk[pos:pos + 1])
        actual = field & FLAG_PROP[propiedad]
        if value and not actual:
            field += FLAG_PROP[propiedad]
        elif not value and actual:
            field -= FLAG_PROP[propiedad]
        return '{}{}{}'.format(field_status_apk[:pos], field, field_status_apk[pos+1:])

    def field_status_rdone(self):
        res = True
        for campo in BINARYPOSITION.keys():
            res = res and (self.read_status(campo, 'done') or not self.read_status(campo, 'req'))
            if not res:
                break
        return res

    def field_status_wdone(self, value=True):
        res = True
        for campo in BINARYPOSITION.keys():
            res = res and self.write_status(campo, 'done', value=value)
        return res


    def write_status_no_usar(self, status_field, campo, propiedad, value=True):
        pos = BINARYPOSITION[campo]
        field = int(status_field[pos:pos+1])
        if value:
            field |= FLAG_PROP[propiedad]
        else:
            field ^= FLAG_PROP[propiedad]
        return field


    def get_model_object(self, values={}):
        res = super().get_model_object(values)
        index = 0
        for sml in self:
            move_id = sml.move_id
            if move_id.tracking != 'none':
                if sml.lot_id:
                    res[index].update(lot_id=self.m2o_dict(sml.lot_id))
                    if sml.read_status('lot_id', 'done'):
                        res[index].update(lot_name=sml.lot_id.name)
                else:
                    res[index].update(lot_id=False)
            index += 1
        return res

    def return_fields(self, mode='tree'):
        return ['id', 'product_uom_qty', 'qty_done', 'location_id', 'location_dest_id', 'lot_id', 'field_status_apk', 'lot_name',
                'package_id', 'result_package_id', 'tracking', 'state', 'removal_priority']

    @api.model
    def remove_line_id(self, values):
        move_id = values['move_id']
        sml_ids = values['sml_ids']
        move_id = self.env['stock.move'].browse(move_id)
        to_unlink = self.browse(sml_ids).unlink()
        move_id._recompute_state()
        values = {'id': move_id, 'model': 'stock.move', 'view': 'form'}
        return self.env['info.apk'].get_apk_object(values)

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
            return res[0]['id']
        domain = domain_base + [('product_id.barcode', '=', code)]
        res = self.search_read(domain, ['id'], limit=1)
        if res:
            return res[0]['id']

        domain = domain_base + [('product_id.default_code', '=', code)]
        res = self.search_read(domain, ['id'], limit=1)
        if res:
            return res[0]['id']
            return self.get_move_line_info_apk({'move_id': res[0]['id']})
        return False

    @api.model
    def get_default_field_status(self, values):
        id = values.get('id', False)
        return self.browse(id).move_id.get_default_field_status()

    @api.model
    def update_sml_field(self, vals):

        message = False
        sml_id = self.browse(vals['sml_id'])
        move_id = self.env['stock.move'].browse(vals['move_id'])
        values = vals.get('values', {})
        default_location = move_id.default_location
        if values.get('new_location_barcode', False):
            location_id = self.env['stock.location'].get_location_from_apk_values(values['new_location_barcode'])
            if location_id:
                sml_id[default_location] = location_id
                sml_id.write_status(default_location, 'done', True)
                move_id.active_location_id = location_id
        elif 'qty_done' in values.keys():
            qty_done = values['qty_done']
            sml_id.qty_done = qty_done
            sml_id.write_status('qty_done', 'done', True)
        elif values.get('new_lot_name', False):
            lot_id = self.get_apk_lot(values['new_lot_name'].upper(), sml_id.product_id)
            ##Busco un lote que tenga la cantidad suficiente. Si hay una cantidad hecha, esa, si no la cantidad del move_line
            need_qty = sml_id.qty_done or sml_id.product_uom_qty
            if lot_id:
                if lot_id.is_enough_to_change(sml_id.location_id, need_qty, strict=True):
                    sml_id.lot_id = lot_id.id
                else:
                    quants = lot_id.is_enough_to_change(move_id[default_location], need_qty, strict=False)
                    if quants:
                        field_status_apk = self._write_status(sml_id['field_status_apk'], default_location, 'done', False)
                        field_status_apk = self._write_status(field_status_apk, 'lot_id', 'done')
                        field_status_apk = self._write_status(field_status_apk, 'qty_done', 'done', False)
                        sml_vals = {'fields_status_apk': field_status_apk,
                                    default_location: quants[0].location_id.id,
                                    'qty_done': sml_id.qty_done}
                        sml_id.write(sml_vals)
                        message = "Se ha cambiado el lote y el {} del moviemiento. Asegurate de que es correcto".format(default_location)
        values = {'id': move_id, 'model': 'stock.move', 'view': 'form'}
        if message:
            values.update(message=message)
        return self.env['info.apk'].get_apk_object(values)

    @api.model
    def update_move_location(self, values):
        move_id = values['move_id']
        sml_ids = values['sml_ids']
        new_loc_id = values['new_loc_id']
        old_loc_id = values['old_loc_id']
        field_location = values['field_location']
        move_id = self.env['stock.move'].browse(move_id)

        if not sml_ids and new_loc_id:
            # Si no me envía listado de lines, los busco por old_loc_id y que no tengan la cantidad hecha
            sml_ids = move_id.move_line_ids.filtered(lambda x: x[field_location]['id'] == old_loc_id and not x.read_status('qty_done', 'done'))
        elif sml_ids:
            # Si envía lineas, pues se la aplica a ellas
            sml_ids = self.browse(sml_ids)
        if sml_ids:
            if new_loc_id:
                # Si hay nueva línea se aplica la nueva
                new_loc_id = self.env['stock.location'].browse(new_loc_id)
                bit_done = True
            else:
                # si borra calcula la original y lo marco como no hecho
                new_loc_id = move_id.compute_active_location_id(field_location)
                bit_done = False

            for line in sml_ids:
                line[field_location] = new_loc_id
                line.write_status(field_location, 'done', bit_done)
                line.write_status(field_location, 'qty_done', bit_done)

        values = {'id': move_id, 'model': 'stock.move', 'view': 'form'}
        move_id.active_location_id = new_loc_id
        return self.env['info.apk'].get_apk_object(values)


    def update_lot_line(self, new_lot_id):
        self.lot_id = False
        new_location = Quant


    @api.model
    def change_line_lot_id(self, values):
        ##Actuliza lotes de los movimientos
        ## Si sml_ids viene de la lísta de moviemitnos si no de la lista de lotes
        move_id = values['move_id']
        sml_ids = values ['sml_ids']
        new_lot_id = values['new_lot_id']
        old_lot_name = values['old_lot_name']
        move_id = self.env['stock.move'].browse(move_id)

        ##old_lot_name : Lotes a borrar. Si solo están en la lista no pasanada
        ## al refrescar se recargan
        ## Por lo tanto, los moviemintos afectados pueden ser los que tengan ese lote o los que vengan directamente decon sml_ids
        if not sml_ids and old_lot_name: ##LISTA DE LOTES
            sml_ids = move_id.move_line_ids.filtered(lambda x: x.lot_id and x.lot_id.name == old_lot_name)
        elif sml_ids:
            sml_ids = self.browse(sml_ids)
        else:
            sml_ids = False

        if new_lot_id:
            lot_id = self.env['stock.production.lot']
            # Busco y o creo el lote
            lot_id = lot_id.find_or_create_lot(new_lot_id, move_id.product_id, not move.picking_type_id.use_existing_lots)
            bit_lot = True
        else:
            lot_id = False
            bit_lot = False

        for line in sml_ids:
            line.lot_id = lot_id
            line.write_status('lot_id', 'done', bit_lot)
            if move_id.active_location_id and bit_lot:
                line.write_status(sml_ids[0][move_id['default_location']], 'done', bit_lot)

        values = {'id': move_id.id, 'model': 'stock.move', 'view': 'form'}
        return self.env['info.apk'].get_apk_object(values)

    @api.multi
    def confirm_bit_qty_done(self, value=True):
        return self.write_status('qty_done', 'done', value)



    @api.model
    def assign_location_to_moves(self, values):
        move_id = values['move_id']
        #sml_ids = values ['sml_ids']
        field_id = values['field']
        barcode = values['barcode']
        confirm = values['confirm']
        active_location_id = values['active_location_id']
        move_id = self.env['stock.move'].browse(move_id)
        location_id = self.env['stock.location'].get_location_from_apk_values(barcode, move_id)
        if not location_id:
            raise ValidationError ('No se ha encontrado una ubicación para {}'.format(barcode))
        move_id.active_location_id = location_id
        default_location = move_id.default_location
        if move_id:
            sml_ids = move_id.move_line_ids.filtered(lambda x: x[default_location].barcode == barcode or not (x.read_status('lot_id', 'done') and x.read_status('qty_done', 'done')))
        if not sml_ids:
            move_id.active_location_id = location_id
            'Creo un movimiento desde esta ubicación para este producto'
            sml_ids = move_id.create_new_sml_id({})
        sml_ids.write_status(default_location, 'done', True)
        sml_ids.write({default_location: location_id.id})
        values = {'id': move_id, 'model': 'stock.move', 'view': 'form'}
        return move_id.get_model_object(values)


    @api.model
    def assign_location_to_moves_bis(self, values):
        move_id = values['move_id']
        sml_ids = values ['sml_ids']
        field_id = values['field']
        barcode = values['barcode']
        confirm = values['confirm']
        active_location_id = values['active_location_id']
        move_id = self.env['stock.move'].browse(move_id)
        ##Busco la ubicación si no me la envían por el codigo de barras
        location_id = self.env['stock.location'].get_location_from_apk_values(barcode, move_id)

        if location_id:
            move_id.active_location_id = location_id
            warning = False
            if sml_ids:
                vals = {field_id: location_id.id}
                for sml in self.env['stock.move.line'].browse(sml_ids):
                    field_status = sml._write_status(sml.field_status_apk, field_id, 'done')
                    if confirm:
                        field_status = sml._write_status(field_status, 'qty_done', 'done', True)
                    vals.update(field_status_apk=field_status)
                    sml.write(vals)
        else:
            warning = 'No se ha encontrado una ubicación para el {}'.format(barcode)
        values = {'id': move_id, 'model': 'stock.move', 'view': 'form'}
        res = self.env['info.apk'].get_apk_object(values)
        if warning:
            if res.get('message'):
                res['message'] = '{}.</br>{}'.format(res['message'], warning)
            else:
                res['message'] = warning
        return res


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
                'display_name': product_id.display_name,
                'state': move_line.state,
                'image': product_id.image_medium,
                'barcode': product_id.barcode,
                'picking_id': {'id': move_line.picking_id.id,
                                'display_name': move_line.picking_id.display_name,
                                'code': move_line.picking_id.picking_type_code},
                'tracking': product_id.tracking,
                'default_code': product_id.default_code,
                'qty_available': product_id.qty_available,
                'location_id': {'id': move_line.location_id.id,
                                'display_name': move_line.location_id.display_name,
                                'barcode': move_line.location_id.barcode},
                'location_dest_id': {'id': move_line.location_dest_id.id,
                                     'display_name': move_line.location_dest_id.display_name,
                                     'barcode': move_line.location_dest_id.barcode},
                'product_uom_qty': move_line.product_uom_qty,
                'uom_move': {'uom_id': move_line.product_uom_id.id, 'name': move_line.product_uom_id.name},
                'qty_done': move_line.qty_done,
                'lot_id': {'id': move_line.lot_id and move_line.lot_id.id or False,
                           'name': move_line.lot_id and move_line.lot_id.name or ''},
                'ready_to_validate': sum(line.qty_done for line in move_line.picking_id.move_line_ids) == sum(line.product_uom_qty for line in move_line.picking_id.move_line_ids)
                }
        return data


    @api.model
    def set_qty_done_from_apk(self, vals):
        move_line_id = vals.get('move_line_id', False)
        qty_done = vals.get('qty_done', False)
        if not move_line_id or not qty_done:
            return {'err': True, 'error': "No se ha enviado la línea o la cantidad a modificar."}
        move_line = self.browse(move_line_id)
        if not move_line:
            return {'err': True, 'error': "La línea introducida no existe."}
        try:
            move_line.update({
                'qty_done': qty_done
            })
            _logger.info("APK. Se ha actualizado el movimeinto {}:{} con cantidad {}".format(move_line.id, move_line.display_name, move_line.qty_done))
            values = {'id': move_id, 'model': 'stock.move', 'view': 'form'}
            res = self.env['info.apk'].get_apk_object(values)
            return True
        except Exception as e:
            _logger.info("APK. Error al actualizar el movimeinto {}:{} con cantidad {}".format(move_line.id,
                                                                                      move_line.display_name,
                                                                                      move_line.qty_done))
            return {'err': True, 'error': e}