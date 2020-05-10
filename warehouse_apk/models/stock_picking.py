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
from odoo.exceptions import UserError
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

    @api.multi
    def compute_field_status(self):
        for pick in self:
            pick.field_status = all(x.field_status == True for x in pick.move_lines)


    def return_fields(self, mode='tree'):
        res = ['id', 'apk_name', 'location_id', 'location_dest_id', 'scheduled_date', 'state', 'sale_id', 'move_line_count', 'picking_type_id', 'default_location', 'field_status']
        if mode == 'form':
            res += ['field_status', 'group_code']
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

        pick = self.browse(values.get('id', False))
        move_id = self.browse(values.get('move_id', False))
        pick.action_done()
        values = {'id': move_id, 'model': 'stock.move', 'view': 'form', 'message': 'El albarán {} esta hecho'.format(pick.name)}
        return self.env['info.apk'].get_apk_object(values)


    @api.model
    def action_assign_pick(self, vals):
        picking = self.browse(vals.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán"}
        res = picking.action_assign()
        return res

    @api.model
    def button_validate_pick(self, vals):
        picking_id = self.browse(vals.get('id', False))
        if not picking_id:
            return {'err': True, 'error': "No se ha encontrado el albarán"}

        ctx = picking_id._context.copy()
        ctx.update(skip_overprocessed_check=True)
        res = picking_id.with_context(ctx).button_validate()
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

    