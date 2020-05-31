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

from odoo import _, api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import time
import pprint
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class StockPicking(models.Model):

    _inherit = ['info.apk', 'stock.picking']
    _name = 'stock.picking'

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.name

    @api.multi
    def compute_move_line_count(self):
        for pick in self:
            pick.move_line_count = len(pick.move_line_ids)

    app_integrated = fields.Boolean(related='picking_type_id.app_integrated')
    move_line_count = fields.Integer('# Operaciones', compute="compute_move_line_count")
    field_status = fields.Boolean(compute="compute_field_status")
    default_location = fields.Selection(related='picking_type_id.group_code.default_location')
    group_code = fields.Selection(related='picking_type_id.group_code.code')
    barcode_re = fields.Char(related='picking_type_id.warehouse_id.barcode_re')
    product_re = fields.Char(related='picking_type_id.warehouse_id.product_re')

    @api.multi
    def compute_field_status(self):
        for pick in self:
            pick.field_status = all(x.field_status == True for x in pick.move_lines)


    def return_fields(self, mode='tree'):
        res = ['id', 'apk_name', 'location_id', 'location_dest_id', 'scheduled_date', 'state', 'sale_id', 'move_line_count', 'picking_type_id', 'default_location', 'field_status', 'priority']
        if mode == 'form':
            res += ['field_status', 'group_code', 'barcode_re', 'product_re']
        return res

    def _compute_picking_count_domains(self):
        # DEBE SER UNA COPIA DE LOS DOMINIOS QUE SE USAN PARA CALCULAR LOS VALORES
        domains = {
            'count_picking_draft': [('state', '=', 'draft')],
            'count_picking_waiting': [('state', 'in', ('confirmed', 'waiting'))],
            'count_picking_ready': [('state', '=', 'assigned')],
            'count_picking': [('state', 'in', ('assigned', 'waiting', 'confirmed'))],
            'count_picking_late': [('scheduled_date', '<', time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)), ('state', 'in', ('assigned', 'waiting', 'confirmed'))],
            'count_picking_backorders': [('backorder_id', '!=', False), ('state', 'in', ('confirmed', 'assigned', 'waiting'))],
        }
        return domains

    @api.model
    def get_picking_list(self, values):
        domain = []
        if values.get('picking_type_id', False):
            domain += [('picking_type_id', '=', values['picking_type_id'])]
        if values.get('domain_name', False):
            domain += self._compute_picking_count_domains()[values['domain_name']]
        if values.get('search', False):
            domain += [('name', 'ilike', values['search'] )]
        if values.get('state', False):
            domain += [('state', '=', values['state']['value'])]
        if not domain and values.get('active_ids'):
            domain += [('id', 'in', values.get['active_ids'])]

        values['domain'] = domain
        return self.get_model_object(values)

    def get_model_object(self, values={}):

        res = super().get_model_object(values=values)
        if values.get('view', 'tree') == 'tree':
            return res
        picking_id = self
        if not picking_id:
            domain = values.get('domain', [])
            limit = values.get('limit', 1)
            move_id = self.search(domain, limit)
            if not picking_id or len(picking_id) != 1:
                return res
        values = {'domain': [('picking_id', '=', picking_id.id)]}
        res['move_lines'] = self.env['stock.move'].get_model_object(values)
        #print ("------------------------------Move lines")
        #pprint.PrettyPrinter(indent=2).pprint(res['move_lines'])
        return res

    @api.model
    def action_done_apk(self, values):
        return self.button_validate_pick(values)
        picking = self.browse(values.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán"}
        res = picking.action_done()
        return True


        pick = self.browse(values.get('id', False))
        move_id = self.browse(values.get('move_id', False))
        pick.action_done()
        values = {'id': move_id, 'model': 'stock.move', 'view': 'form', 'message': 'El albarán {} esta hecho'.format(pick.name)}
        return self.env['info.apk'].get_apk_object(values)


    @api.model
    def action_assign_apk(self, vals):
        picking = self.browse(vals.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán"}
        res = picking.action_assign()
        return res

    @api.model
    def do_unreserve_apk(self, vals):

        picking = self.browse(vals.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán"}
        res = picking.do_unreserve()
        return True


    @api.model
    def button_validate_pick(self, vals):
        picking_id = self.browse(vals.get('id', False))
        if not picking_id:
            return {'err': True, 'error': "No se ha encontrado el albarán"}
        if all(move_line.qty_done == 0 for move_line in picking_id.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel'))):
            raise ValidationError ('No hay ninguna cantidad hecha para validar')
        ctx = picking_id._context.copy()
        ctx.update(skip_overprocessed_check=True)
        return picking_id.with_context(ctx).button_validate()

        try:
            if res:
                if res['res_model'] == 'stock.immediate.transfer':
                    wiz =  self.env['stock.immediate.transfer'].with_context(res['context']).browse(res['res_id'])
                    res_inm = wiz.process()

                    if res_inm['res_model'] == 'stock.backorder.confirmation':
                        wiz = self.env['stock.backorder.confirmation'].with_context(res_inm['context']).browse(res_inm['res_id'])
                        res_bord = wiz._process()

                if res['res_model'] == 'stock.backorder.confirmation':
                        wiz = self.env['stock.backorder.confirmation'].with_context(res['context']).browse(res['res_id'])
                        res_boc = wiz._process()
            return {'err': False, 'values': {'id': picking_id.id, 'state': picking_id.state}}
        except Exception as e:
            return {'err': e}


    @api.model
    def force_set_qty_done_apk(self, vals):
        picking = self.browse(vals.get('id', False))
        field = vals.get('field', False)
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán."}

        ctx = self._context.copy()
        ctx.update(model_dest="stock.move.line")
        ctx.update(field=field)
        res = picking.with_context(ctx).force_set_qty_done()
        return True

    @api.model
    def force_reset_qties_apk(self, vals):
        picking = self.browse(vals.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán."}
        ctx = self._context.copy()
        ctx.update(reset=True)
        res = picking.with_context(ctx).force_set_qty_done()
        return True

    @api.model
    def process_qr_lines(self, vals):
        qr_codes = self.browse(vals.get('qr_codes', False))
        if not qr_codes:
            return {'err': True, 'error': "No se han recibido datos del código QR."}
        print(qr_codes)
        return True

    @api.model
    def find_pick_by_name(self, vals):
        domain = [('name', 'ilike', vals['name'])]
        res = self.search_read(domain, ['id'], limit=1)
        if res:
            print("------------- Busco el albarán {} y devuelvo  el id".format(vals['name'], res[0]['id']))
            return res[0]['id']
        print("------------- Busco el albarán {} y no encuentro nada".format(vals['name']))
        return False

    @api.model
    def find_serial_for_move(self, vals):
        lot_name = vals.get('lot_id', False)
        picking_id = vals.get('picking_id', False)
        remove = vals.get('remove', False)
        if not picking_id:
            return
        if not lot_name:
            return
        lot_names = lot_name.split(',')
        for lot_name in lot_names:
            lot = self.env['stock.production.lot'].search([('name', '=', lot_name)], limit=1)
            if lot:
                res = self.serial_for_move(picking_id, lot, remove)
                if res:
                    move = res
        if move:
            move._recompute_state()
            return move.get_model_object()
        return False

    @api.model
    def serial_for_move(self, picking_id, lot, remove):
        lot_id = lot.id
        product_id = lot.product_id.id
        new_location_id = lot.compute_location_id()

        domain = [('picking_id', '=', picking_id), ('product_id', '=', product_id)]

        if False and remove:
            domain += [('lot_id', '=', lot_id)]
            line = self.env['stock.move.line'].search(domain, limit=1, order='lot_id desc')
            line.qty_done = 0
            line.write_status('lot_id', 'done', False)
            line.write_status('qty_done', 'done', False)
        else:
            # caso 1. COnfirmar el lote que hay
            lot_domain = domain + [('lot_id', '=', lot_id)]
            line = self.env['stock.move.line'].search(lot_domain, limit=1, order='lot_id desc')
            if line:
                ## si es lote +1 , si es serial = 1
                if line.product_id.tracking == 'serial':
                    line.qty_done = 1
                else:
                    line.qty_done += 1
                line.write_status('lot_id', 'done', True)
                line.write_status('qty_done', 'done', True)
            else:
                # Caso 2. Hay una vacía con lot_id = False:
                lot_domain = domain + [('lot_id', '=', False)]
                line = self.env['stock.move.line'].search(lot_domain, limit=1, order= 'lot_id desc')
                if not line:
                    lot_domain = domain + [('lot_id', '!=', lot_id), ('qty_done', '=', 0)]
                    line = self.env['stock.move.line'].search(lot_domain, limit=1, order='lot_id desc')
                if line:
                    move = line.move_id
                    line.unlink()
                    result = move._update_reserved_quantity(1, 1, location_id=move.location_id, lot_id=lot, strict=False)
                    if result == 0:
                        raise UserError ('No se ha podido reservar el lote {}. Comprueba que no está    en otro movimiento'.format(lot.name))
                    lot_domain = domain + [('lot_id', '=', lot_id)]
                    line = self.env['stock.move.line'].search(lot_domain, limit=1, order='lot_id desc')
                    if line:
                        line.qty_done = 1
                        line.write_status('lot_id', 'done', True)
                        line.write_status('qty_done', 'done', True)
        move = line.move_id
        ##devuelvo un objeto movimietno para actualizar la vista de la app
        if not move:
            return False
        return move






