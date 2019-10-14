# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    forced_move_line = fields.Boolean('Forced move line')
    pda_done = fields.Boolean('Pda done')
    need_check = fields.Boolean(related='location_id.need_check')
    need_dest_check = fields.Boolean(related='location_dest_id.need_dest_check')
    original_location_short_name = fields.Char(related='location_id.name')
    final_location_short_name = fields.Char(related='location_dest_id.name')
    product_short_name = fields.Char(related='product_id.product_tmpl_id.name')
    product_barcode = fields.Char(related='product_id.barcode')
    product_need_check = fields.Boolean(related="product_id.product_tmpl_id.need_check")


    @api.model
    def create_moves_from_serial(self, vals):

        move_id = self.browse(vals.get('move_id', False))
        serial_name = vals.get('lot_ids', [])[0]
        serial_obj = self.env['stock.production.lot']

        serial = serial_obj.search([('name', '=', serial_name['name'])])
        if not serial:
            serial = serial_obj.create({'name': serial_name['name'], 'product_id': move_id.product_id.id})
        move_id.write({'lot_id': serial.id, 'qty_done': serial_name['qty']})
        return True

    @api.multi
    def unlink(self):
        return super(StockMoveLine, self).unlink()

    @api.model
    def get_apk_vals(self, type='normal'):

        if not self:
            return False
        vals = {'id': self.id,
                'name': self.display_name,
                'state': self._fields['state'].convert_to_export(self.state, self),
                'model': 'stock.move.line'
        }

        if type != 'min':
            vals.update({
                'pda_done': True if self.state == 'done' or self.qty_done > 0 else False,
                'user_id': self.picking_id.user_id.get_apk_vals('min'),
                'product_id': self.product_id.get_apk_vals('min'),
                'product_uom_qty': self.product_uom_qty,
                'qty_done': self.qty_done,
                'ordered_qty': self.ordered_qty,
                'location_id': self.location_id.get_apk_vals(),
                'location_dest_id': self.location_dest_id.get_apk_vals(),
                'product_uom_id': self.product_uom_id.get_apk_vals('min'),
                'package_id': self.package_id.get_apk_vals('min'),
                'result_package_id': self.result_package_id.get_apk_vals('min'),
                'lot_id': self.lot_id.get_apk_vals('min'),
                'picking_id': self.picking_id and self.picking_id.get_apk_vals('min'),
                'product_qty': self.product_qty,
                'has_tracking': self.product_id._fields['tracking'].convert_to_export(self.product_id.tracking,
                                                                                  self.product_id),
                'uom_to_uos': False,
                'checked': {
                    'move_id': True,
                    'product_id': True if self.lot_id or self.package_id else False,
                    'lot_id': True if self.product_id.tracking == 'none' else False,
                    'package_id': False if self.package_id else True,
                    'location_id': False if self.location_id.need_check else True,
                    'location_dest_id': False if self.location_dest_id.need_dest_check else True,
                    'package_dest_id': False if self.location_dest_id.need_package else True,
                    'qty': False if self.product_id.need_qty_check else True
                }
            })
            if 'uos_id' in self._fields:
                vals.update({
                    'uos_id': self.uos_id.get_apk_vals('min'),
                    'uom_to_uos': self.uos_id.factor/self.product_uom_id.factor
                })

        if type == 'form':
            vals.update({
                'product_id': self.product_id.get_apk_vals(),
                'move_id': (self.move_id.id, self.move_id.name),
                'ordered_qty': self.ordered_qty,
                'reference': self.reference,
                'is_locked': self.is_locked,
                'to_loc': self.to_loc,
                'in_entire_package': self.in_entire_package,

            })
        print ('Stock Move: valores {} \n {}'.format(type, vals))
        return vals

    @api.model
    def set_as_pda_done(self, vals):
        next_move_id = False
        move_id = self.browse(vals.get('move_id', False))
        orig_vals = vals.get('vals', {})
        if not move_id:
            return {'err': True, 'error': "No se ha encontrado el movimiento"}

        if move_id.state in ['done', 'cancel']:
            return {'err': True, 'error': "Estado incorrecto"}

        pda_done = orig_vals['pda_done']
        move_vals = {}
        if pda_done:
            move_vals['qty_done'] = orig_vals.get('qty_done', 0.00) or move_id.product_uom_qty
        else:
            move_vals['qty_done'] = 0.00
        ##SOLO ESCRIBO LA CANTIDAD.
        ## Qty > 0.00 está marcado como realizado, si no esta pendiente
        res = move_id.write(move_vals)
        if not res:
            return {'err': True, 'error': "Error al marcar la operación"}
        ret_vals = {'object': object, 'next_move_id': next_move_id}
        next_move_id = vals.get('next_move_id', False)
        if next_move_id:
            object = 'stock.move.line'
        else:
            next_move_id = move_id.get_next_move_id(move_id.picking_id.move_line_ids.filtered(lambda x: not x.pda_done))
            if next_move_id:
                object = 'stock.move.line'
            else:
                object = 'stock.picking'
                next_move_id = False

        ret_vals = {'object': object, 'next_move_id': next_move_id}
        return ret_vals

    @api.model
    def get_stock_move_line_pda(self, values):

        line_id = values.get('line_id', False)
        if not line_id:
            return []
        line = self.env['stock.move.line'].browse(line_id)
        vals = line.get_apk_vals(type='form')
        return vals

    @api.multi
    def get_available_move_line_lot_pda(self, values=[]):
        self.browse(id)
        move_id = values.get('move_id', False)
        if not move_id:
            return []
        return self.env['stock.move'].browse(move_id).get_available_move_line_lot(self)

    @api.model
    def get_next_move_id(self, moves, reverse=False):

        if reverse:
            moves = reversed(moves)
        act_move = False
        prev_move = False
        next_move = False
        for move in moves:
            if next_move:
                continue
            if not act_move and not self.id == move.id:
                act_move = move.id

            if prev_move and not next_move:
                next_move = prev_move
            if self.id == move.id:
                prev_move = self.id
        return next_move or act_move
    
    @api.model
    def set_as_pda_done_single_line(self, vals):
        if isinstance(vals['id'], int):
            move_line_obj = self.browse(vals['id'])
            result = move_line_obj.write({'qty_done': move_line_obj.ordered_qty})
            return result 
        else:
            for move in vals['id']:
                move_line_obj = self.browse(move['id'])
                result = move_line_obj.write({'qty_done': move_line_obj.ordered_qty})
            return result     

    @api.model
    def update_line_values_apk(self, vals):
        for line in vals:
            line_obj = self.browse(line['id'])
            result = line_obj.write({'qty_done': line['qty_done']})
        return result     


class StockMove(models.Model):

    _inherit = "stock.move"


    @api.model
    def get_component_info(self, model_id, model):
        move = self.browse(model_id)

        data = move.get_apk_vals()
        return data

    @api.multi
    def _get_forced_move_line(self):
        for move in self:
            move.forced_move_line = any(line.forced_move_line for line in move.move_line_ids)

    forced_move_line = fields.Boolean('Forced move line', compute=_get_forced_move_line)
    need_check = fields.Boolean(related='location_id.need_check')
    need_dest_check = fields.Boolean(related='location_dest_id.need_dest_check')

    def _action_assign(self):

        res = super(StockMove, self)._action_assign()
        if not self._context.get('forced_move_line', False):
            return res

        ctx = self._context.copy()
        ctx.update(bypass_reservation_update=True, forced_move_line=True)

        not_reserved_moves = self.with_context(ctx).filtered(lambda m: m.state in ['confirmed', 'waiting', 'partially_available'] and (m.product_uom_qty - m.reserved_availability > 0.001))
        if not not_reserved_moves:
            return res
        print("Entro para crear los {}".format(not_reserved_moves.mapped('product_id')))
        message =_('The picking <a href=# data-oe-model=stock.picking data-oe-id=%d>%s</a> has been forced.<ul>') % (not_reserved_moves[0].picking_id.id, not_reserved_moves[0].picking_id.name)
        for move in not_reserved_moves:
            missing_reserved_uom_quantity = move.product_uom_qty - move.reserved_availability
            missing_reserved_quantity = move.product_uom._compute_quantity(missing_reserved_uom_quantity,
                                                                           move.product_id.uom_id,
                                                                           rounding_method='HALF-UP')

            if missing_reserved_quantity:
                # create the move line(s) but do not impact quants
                if move.product_id.tracking == 'serial' and (
                        move.picking_type_id.use_create_lots or move.picking_type_id.use_existing_lots):
                    for i in range(0, int(missing_reserved_quantity)):
                        self.env['stock.move.line'].create(move._prepare_move_line_vals(quantity=1))

                    message = '{}{}'.format(message, _('<li>The move <a href=# data-oe-model=stock.move data-oe-id=%d>%s</a> has been forced (%s %s) .</li>') % (move.id, move.product_id.display_name, missing_reserved_quantity, move.product_uom.name))
                else:
                    to_update = move.move_line_ids.filtered(lambda ml: ml.product_uom_id == move.product_uom and
                                                                       ml.location_id == move.location_id and
                                                                       ml.location_dest_id == move.location_dest_id and
                                                                       ml.picking_id == move.picking_id and
                                                                       not ml.lot_id and
                                                                       not ml.package_id and
                                                                       not ml.owner_id)
                    if to_update:
                        to_update[0].product_uom_qty += missing_reserved_uom_quantity
                    else:
                        self.env['stock.move.line'].create(move._prepare_move_line_vals(quantity=missing_reserved_quantity))
                        message = '{}{}'.format(message,_('<li>The move <a href=# data-oe-model=stock.move data-oe-id=%d>%s</a> has been forced  (%s %s) .</li>') % (move.id, move.product_id.display_name, missing_reserved_quantity, move.product_uom.name))
        message = '{}{}'.format(message, '</ul>')
        not_reserved_moves[0].picking_id.message_post(message)

        return res

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super(StockMove, self)._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        if self._context.get('forced_move_line', False):
            vals.update(forced_move_line=True)
            print(vals)
        return vals

    @api.multi
    @api.depends('move_line_ids.product_qty')
    def _compute_reserved_availability(self):
        """ Fill the `availability` field on a stock move, which is the actual reserved quantity
        and is represented by the aggregated `product_qty` on the linked move lines. If the move
        is force assigned, the value will be 0.
        """
        new_self = self.filtered(lambda x: not x.forced_move_line)
        res = super(StockMove, new_self)._compute_reserved_availability()
        force_self = self - new_self
        if force_self:
            ctx = self._context.copy()
            ctx.update(bypass_reservation_update=True, forced_move_line=True)
            force_self = force_self.with_context(ctx)
            result = {data['move_id'][0]: data['product_qty'] for data in
                      self.env['stock.move.line'].read_group([('move_id', 'in', force_self.ids), ('forced_move_line', '=', True)], ['move_id', 'product_qty'],
                                                             ['move_id'])}
            for rec in force_self:
                rec.reserved_availability = rec.product_id.uom_id._compute_quantity(result.get(rec.id, 0.0),
                                                                                    rec.product_uom,
                                                                                    rounding_method='HALF-UP')
        return res

    def _do_unreserve(self):

        res = super(StockMove, self.filtered(lambda x: not x.forced_move_line))._do_unreserve()
        ctx = self._context.copy()
        ctx.update(bypass_reservation_update=True, forced_move_line=True)

        forced_moves = self.with_context(ctx).filtered(lambda x: x.forced_move_line)
        if not forced_moves:
            return res
        moves_to_unreserve = self.env['stock.move']
        for move in forced_moves:
            if move.state == 'cancel':
                # We may have cancelled move in an open picking in a "propagate_cancel" scenario.
                continue
            if move.state == 'done':
                if move.scrapped:
                    # We may have done move in an open picking in a scrap scenario.
                    continue
                else:
                    raise UserError(_('Cannot unreserve a done move'))
            moves_to_unreserve |= move

        moves_to_unreserve.mapped('move_line_ids').with_context(ctx).unlink()
        self._recompute_state()

        return True

    @api.model
    def get_stock_move_line_pda(self, values):

        line_id = values.get('line_id', False)
        if not line_id:
            return []
        line = self.env['stock.move'].browse(line_id)
        vals = line.get_apk_vals(type='form')
        return vals


    @api.model
    def get_apk_vals(self, type='normal'):
        if not self:
            return False
        vals = {'id': self.id,
                'name': self.display_name,
                'state': self._fields['state'].convert_to_export(self.state, self),
                'model': 'stock.move',
                }

        if type != 'min':
            vals.update({
                'pda_done': True if self.state == 'done' or self.quantity_done > 0 else False,
                'user_id': self.picking_id.user_id.get_apk_vals('min'),
                'inventory_id': self.inventory_id or False,
                'product_id': self.product_id.get_apk_vals('min'),
                'product_uom_qty': self.product_uom_qty,
                'qty_done': self.quantity_done,
                'location_id': self.location_id.get_apk_vals('min'),
                'location_dest_id': self.location_dest_id.get_apk_vals(),
                'product_uom_id': self.product_uom.get_apk_vals('min'),
                'package_id': self.env['stock.quant.package'].get_apk_vals('min'),
                'result_package_id': self.env['stock.quant.package'].get_apk_vals('min'),
                'lot_id': self.env['stock.production.lot'].get_apk_vals('min'),
                'picking_id': self.picking_id and self.picking_id.get_apk_vals('min'),
                'product_qty': self.product_uom_qty - self.reserved_availability,
                'has_tracking': self.product_id._fields['tracking'].convert_to_export(self.product_id.tracking,
                                                                                  self.product_id),
                'uom_to_uos': False,
                'checked': {
                    'move_id': True,
                    'product_id': False,
                    'lot_id': True if self.product_id.tracking == 'none' else False,
                    'package_id': False ,
                    'location_id': False if self.location_id.need_check else True,
                    'location_dest_id': False if self.location_dest_id.need_dest_check else True,
                    'package_dest_id': False if self.location_dest_id.need_package else True,
                    'qty': False if self.product_id.need_qty_check else True
                }
            })
            if 'uos_id' in self._fields:
                vals.update({
                    'uos_id': self.uos_id.get_apk_vals('min'),
                    'uom_to_uos': self.uos_id.factor / self.product_uom_id.factor
                })

        if type == 'form':
            vals.update({
                'move_id': (False, False),
                'product_id': self.product_id.get_apk_vals(),
                'ordered_qty': self.ordered_qty,
                'reference': self.reference,
                'is_locked': self.is_locked,
                #'to_loc': self.to_loc,
                #'in_entire_package': self.in_entire_package,

            })
        print('Stock Move: valores {} \n {}'.format(type, vals))
        return vals

    @api.model
    def create_moves_from_serial(self, vals):
        move_id = self.browse(vals.get('move_id', False))
        move_vals = {'product_id': move_id.product_id.id,
                     'picking_id': move_id.picking_id.id,
                     'move_id': move_id.id,
                     'location_id': move_id.location_id.id,
                     'location_dest_id': move_id.location_dest_id.id,
                     'product_uom_qty': 0,
                     'product_uom_id': move_id.product_uom.id}

        serial_ids = vals.get('lot_ids', [])
        serial_obj = self.env['stock.production.lot']
        for serial_name in serial_ids:
            serial = serial_obj.search([('name', '=', serial_name['name'])])
            if not serial:
                serial = serial_obj.create({'name': serial_name['name'], 'product_id': move_id.product_id.id})
            move_vals.update(lot_id = serial.id)
            self.env['stock.move.line'].create(move_vals).write({'qty_done': serial_name['qty']})
        move_id._action_assign()
        return True

    @api.model
    def get_qty_available_before_creation(self, vals):

        product_id, location_id = vals['product_id'], vals['location_id']

        product_id = self.env['product.product'].browse(product_id)
        location_id = self.env['stock.location'].browse(location_id)

        qty_available = product_id.with_context(location=location_id.id).qty_available_global

        return qty_available

    @api.model
    def create_from_pda(self, vals):

        product_id, location_id = vals['product_id'], vals['location_id']
        product_uom_qty, location_dest_id = vals['product_uom_qty'], vals['location_dest_id']
        name, qty_done = vals['name'], vals['qty_done']
        product_obj = self.env['product.product'].browse(vals['product_id'])
        product_uom = product_obj.uom_id.id

        result = self.env['stock.move'].create({
            'name': name,
            'product_id': product_id,
            'product_uom_qty': product_uom_qty,
            'product_uom': product_uom,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'procure_method': 'make_to_stock'
        })

        result.action_confirm_for_pda()

        return result.id

    @api.model
    def search_for_quants_apk(self, vals):

        stock_move = self.env['stock.move'].browse(vals)
        stock_move.action_assign_for_pda()

        return True

    @api.model
    def force_quants_for_apk(self, vals):

        stock_move = self.env['stock.move'].browse(vals)
        stock_move.force_assign_for_pda()

        return True

    @api.model
    def move_validation_from_apk(self, vals):
        stock_move = self.env['stock.move'].browse(vals)
        stock_move.action_done_for_pda()
        return True
    
    @api.model
    def create_new_picking_from_moves_apk(self, vals):
        move_lines = []
        for move in vals['moves']:
            move_lines.append(move['id'])

        picking = self.env['stock.picking'].create({
            'location_id' : vals['location_id'],
            'location_dest_id': vals['location_dest_id'],
            'picking_type_id': vals['picking_type_id'],
            'move_type': 'direct'
        })

        for move in vals['moves']:
            line = self.env['stock.move'].browse(move['id']).write({
                'picking_id': picking.id
            })

        picking.action_assign()

        return picking.id

    @api.model
    def create_for_picking(self, vals):

        product_id, location_id = vals['product_id'], vals['location_id']
        product_uom_qty, location_dest_id = vals['product_uom_qty'], vals['location_dest_id']
        name, qty_done = vals['name'], vals['qty_done']
        product_obj = self.env['product.product'].browse(vals['product_id'])
        product_uom, picking_id = product_obj.uom_id.id, vals['picking_id']

        result = self.env['stock.move'].create({
            'name': name,
            'product_id': product_id,
            'product_uom_qty': product_uom_qty,
            'product_uom': product_uom,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'procure_method': 'make_to_stock',
            'picking_id': picking_id
        })

        return result.id