# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

DEFAULT_MOVE_FIELDS = ['id', 'name', 'product_id', 'product_uom_qty', 'location_id',
                       'location_dest_id', 'state', 'product_uom']
DEFAULT_MOVE_LINE_FIELDS = ['id', 'move_id', 'product_id', 'product_uom_qty', 'qty_done', 'location_id',
                            'location_dest_id', 'state', 'product_uom_id', 'package_id', 'result_package_id',
                            'lot_id', 'lot_name']
DEFAULT_FIELDS = ['id', 'name', 'state', 'scheduled_date', 'delayed']

class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    ## HASTA AQUI

    show_in_pda = fields.Boolean("Show in PDA", help="If checked, this picking type will be shown in pda")
    short_name = fields.Char("Short name in PDA", help="Short name to show in PDA")
    #need_confirm = fields.Boolean("Need confirm in PDA", help="If checked, this force to process with button after all requeriments done")
    #process_from_tree = fields.Boolean("Process from pda tree ops", help="If checked, allow to process op with default values from pick tree ops in pda")



class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.model
    def get_component_info(self, model_id, model='stock.picking'):
        picking = self.browse(model_id)

        if picking.location_id:
            location_id = {
                '0': picking.location_id.id,
                '1': picking.location_id.name
            }
        else:
            location_id = False

        if picking.location_dest_id:
            location_dest_id = {
                '0': picking.location_dest_id.id,
                '1': picking.location_dest_id.name
            }
        else:
            location_dest_id = False
        
        if picking.move_lines:
            move_lines = picking.move_lines.ids
            move_count = len(picking.move_lines)
        else:
            move_lines = False
            move_count = 0

        if picking.move_line_ids:
            move_line_ids = []
            cont = 0
            for line in picking.move_line_ids:
                line_data = self.env['stock.move.line'].get_component_info(line.id, 'stock.move.line')
                line_data.update({
                    'index': cont
                })
                move_line_ids.append(line_data)
                cont += 1
            move_done_count = len(picking.move_line_ids.filtered(lambda x: x.state == 'done' or x.state == 'assigned'))
        else:
            move_line_ids = False
            move_done_count = 0

        if picking.partner_id:
            partner_id = {
                '0': picking.partner_id.id,
                '1': picking.partner_id.name
            }
        else:
            partner_id = False

        if picking.picking_type_id:
            picking_type_id = {
                '0': picking.picking_type_id.id,
                '1': picking.picking_type_id.name,
                '2': picking.picking_type_id.code
            }
        else:
            picking_type_id = False

        data = {
            'id': picking.id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'model': 'stock.picking',
            'move_count': move_count,
            'move_done_count': move_done_count,
            'move_lines': move_lines,
            'moves': move_line_ids,
            'move_line_ids': move_line_ids,
            'note': picking.note,
            'name': picking.name,
            'partner_id': partner_id,
            'picking_type_id': picking_type_id,
            'scheduled_date': picking.scheduled_date,
            'state': picking.state
        }
        return data

    @api.multi
    def get_need_force_availability(self):
        for pick in self:
            pick.need_force = pick.state in ('waiting', 'confirmed') and any(move.reserved_availability == 0 for move in pick.move_lines)

    @api.multi
    def get_delayed_val(self):
        today = fields.Datetime.now()[0:10]
        now = fields.Datetime.now()
        for pick in self:
            if pick.state in ('cancel', 'done') or pick.scheduled_date > now:
                delayed = 0
            elif pick.scheduled_date > today:
                delayed = 1
            else:
                delayed = 2
            pick.delayed = delayed


    user_id = fields.Many2one('res.users', 'Operator')
    need_force = fields.Boolean('Need force availability', compute="get_need_force_availability")
    delayed = fields.Integer('Delayed type', compute="get_delayed_val")




    @api.model
    def get_apk_vals(self, type='normal'):
        if not self:
            return False

        vals = {'id': self.id,
                'name': self.name}
        ops = self.move_lines.mapped('move_line_ids')
        if type != 'min':
            vals.update({'state': self._fields['state'].convert_to_export(self.state, self),
                   'scheduled_date': self.scheduled_date,
                   'delayed': self.delayed,
                   'moves_done': ops.filtered(lambda x: x.qty_done > 0.00).ids,
                   'moves_waiting': ops.filtered(lambda x: x.qty_done == 0.00).ids,
                   'user_id': self.user_id and self.user_id.get_apk_vals(),
                   'location_id': self.location_id and self.location_id.get_apk_vals('min'),
                   'location_dest_id': self.location_dest_id and self.location_dest_id.get_apk_vals('min')})

        print('Location: valores {} \n {}'.format(type, vals))
        return vals


    @api.model
    def get_picking_pda(self, values):

        picking_id = values.get('picking_id', False)
        if not picking_id:
            return []
        picking_id = self.env['stock.picking'].browse(picking_id)


        picking = picking_id.get_apk_vals('form')

        domain = [('picking_id', '=', picking_id.id)]
        moves_obj = self.env['stock.move.line'].search(domain, limit=100)
        moves=[]
        for move_obj in moves_obj:
            moves.append(move_obj.get_apk_vals())

        domain.append(('state', 'in', ('confirmed', 'partially_available')))
        moves_obj = self.env['stock.move'].search(domain, limit=100)

        for move_obj in moves_obj:
            moves.append(move_obj.get_apk_vals())

        picking['moves'] = moves
        print ("PICKING: \n{}".format(picking))
        return picking


    @api.multi
    def force_availibility(self):
        ctx = self._context.copy()
        ctx.update(forced_move_line=True)
        res = self.with_context(ctx).action_assign()
        self._compute_state()
        return res

    @api.model
    def button_validate_from_pda(self, vals):

        picking_id = self.browse(vals.get('picking_id', False))
        if not picking_id:
            return {'err': True, 'error': "No se ha encontrado el albarán"}

        ctx = picking_id._context.copy()
        ctx.update(skip_overprocessed_check=True)
        res = picking_id.with_context(ctx).button_validate()
        if res:
            if res['res_model'] == 'stock.immediate.transfer':
                wiz =  self.env['stock.immediate.transfer'].with_context(res['context']).browse(res['res_id'])
                res_inm = wiz.process()

                if res_inm['res_model'] == 'stock.backorder.confirmation':
                    wiz = self.env['stock.backorder.confirmation'].with_context(res_inm['context']).browse(res_inm['res_id'])
                    wiz._process()

            if res['res_model'] == 'stock.backorder.confirmation':
                    wiz = self.env['stock.backorder.confirmation'].with_context(res['context']).browse(res['res_id'])
                    wiz._process()
        return {'err': False, 'values': {'id': picking_id.id, 'state': picking_id.state}}