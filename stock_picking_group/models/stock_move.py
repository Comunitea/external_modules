# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta



class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

class StockMove(models.Model):

    _inherit = "stock.move"

    need_force_pick = fields.Boolean('Picking auto',
                                     help='If checked, create picking when run procurement, (odoo default). From sale order',
                                     default=False, copy=True)

    pick_state = fields.Selection([
        ('draft', 'Draft'),
        ('error',  'Error'),
        ('waiting', 'Waiting (draft, move or availability'),
        ('assigned', '(Partially) Available'),
        ('picked', 'Picked'),
        ('done', 'Done')], string='Pick status',

        help="* Waiting: Move waiting. Not picked allowed.\n"
             "* Available: Move is (partially) available. Can be picked.\n"
             "* Picked: Move picked"
             "* Error: Move picked and not available.\n"
        )

    @api.multi
    def action_force_assign_picking(self, force=True):

        ctx = self._context.copy()
        ctx.update(force_assign_pick=force)
        return self.with_context(ctx)._assign_picking()


    def _assign_picking(self):

        if self.need_force_pick and not self._context.get('force_assign_pick', False):
            self._action_assign()
            return

        super()._assign_picking()
        for move in self:
            move.move_line_ids.write({'picking_id': move.picking_id.id})

    def _get_new_picking_domain(self):
        vals = super(StockMove, self)._get_new_picking_domain()
        if self.need_force_pick and self._context.get('force_pick', False):
            vals += [('group_pick', '=', True)]
        return vals

    def _get_new_picking_values(self):
        """ Prepares a new picking for this move as it could not be assigned to
        another picking. This method is designed to be inherited. """
        """ VALORES ORIGINALES
            'origin': self.origin,
            'company_id': self.company_id.id,
            'move_type': self.group_id and self.group_id.move_type or 'direct',
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
        }"""

        vals = super()._get_new_picking_values()
        if self.need_force_pick and self._context.get('force_pick', False):
            vals.update(group_pick=True)
        return vals

    def picking_type_sust(self, old, new):
        if old.warehouse_id and (new.warehouse_id and new.warehouse_id != old.warehouse_id):
            return False
        if not old.warehouse_id and new.warehouse_id:
            return False
        if old.code != new.code:
            return False
        return True

    def _prepare_move_split_vals(self, qty):

        vals = super()._prepare_move_split_vals(qty)
        if self._context.get('default_location_id', False):
            vals.update(location_id = self['location_id'].id)

        if self._context.get('default_location_dest_id', False):
            vals.update(location_id = self['location_dest_id'].id)

        return vals

    def check_new_location(self, location='location_id'):
        ##COMPRUBA Y ESTABLECE LA NUEVA UBICACIÓN DE ORIGEN DEL MOVIMIENTO Y CAMBIA EL PICKING_TYPE EN CONSECUENCIA

        if not self.move_line_ids:
            return
        default_picking_type_id = self.picking_type_id
        move_loc = self[location]
        #saco las posibles ubicaciones con albaran de las operaciones
        new_mov_locs = [line[location]._get_location_type_id() for line in self.move_line_ids]
        print ('Solo hay: {}'.format(new_mov_locs))
        # Si solo hay una, la nueva ubicación del movimiento es la de la operación
        if len(new_mov_locs) == 1:
            if new_mov_locs != self[location]:
                self.write({location: new_mov_locs[0]._get_location_type_id().id,
                            'picking_type_id': new_mov_locs[0].picking_type_id.id})
        elif new_mov_locs:
            for loc in new_mov_locs:
                moves_loc = self.move_line_ids.filtered(lambda x: x[location]._get_location_type_id().id == loc.id and x[location]._get_location_type_id().id != self[location].id)
                if moves_loc:
                    qty_loc = sum(ml.product_uom_qty for ml in moves_loc)
                    picking_type_id = loc.picking_type_id or default_picking_type_id
                    ctx = self._context.copy()
                    ctx['default_{}'.format(location)] = loc.id
                    ctx['default_picking_type_id'] = picking_type_id.id
                    new_move_id = self.with_context(ctx)._split(qty_loc)
                    self._do_unreserve()
                    new_move = self.env['stock.move'].browse(new_move_id)
                    new_move._action_assign()
                    #new_move.check_new_location(location)


            if self.product_uom_qty>0:
                self._action_assign()
                self.check_new_location(location)
            else:
                self.unlink()




    def _action_assign(self):

        super(StockMove, self)._action_assign()

        assigned_moves = self.filtered(lambda x: x.state in ('assigned', 'partially_available'))
        ctx = self._context.copy()
        ctx.update(force_pick=True)
        for move in assigned_moves.with_context(ctx):
            move.check_new_location()


    @api.onchange('picking_id', 'state')
    def on_change_pick_state(self):
        for move in self:
            if move.state == 'draft':
                move.pick_state = move.state
                move.picking_id = False
            elif move.state == 'done':
                move.pick_state = move.state
            elif not move.picking_id:
                if move.state in ('partially_available', 'assigned'):
                    move.pick_state = 'assigned'
                else:
                    move.pick_state = 'waiting'
            elif move.picking_id:
                if move.state in ('partially_available', 'assigned'):
                    move.pick_state = 'picked'
                else:
                    move.pick_state = 'error'





class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):

        vals = super()._get_stock_move_values(product_id=product_id,
                                              product_qty=product_qty,
                                              product_uom=product_uom,
                                              location_id=location_id,
                                              name=name,
                                              origin=origin,
                                              values=values,
                                              group_id=group_id)

        if values.get('sale_line_id', False):
            sol = self.env['sale.order.line'].browse(values['sale_line_id'])
            vals.update(need_force_pick=sol.order_id.need_force_pick)
        return vals

        # VALORES ORIGINALES:
        #     POR DEFECTO
        #     values.setdefault('company_id', self.env['res.company']._company_default_get('procurement.group'))
        #     values.setdefault('priority', '1')
        #     values.setdefault('date_planned', fields.Datetime.now())
        #     ORIGINALES PARA MOVE
        #     'name': name[:2000],
        #     'company_id': self.company_id.id or self.location_src_id.company_id.id or self.location_id.company_id.id or values['company_id'].id,
        #     'product_id': product_id.id,
        #     'product_uom': product_uom.id,
        #     'product_uom_qty': qty_left,
        #     'partner_id': self.partner_address_id.id or (values.get('group_id', False) and values['group_id'].partner_id.id) or False,
        #     'location_id': self.location_src_id.id,
        #     'location_dest_id': location_id.id,
        #     'move_dest_ids': values.get('move_dest_ids', False) and [(4, x.id) for x in values['move_dest_ids']] or [],
        #     'rule_id': self.id,
        #     'procure_method': self.procure_method,
        #     'origin': origin,
        #     'picking_type_id': self.picking_type_id.id,
        #     'group_id': group_id,
        #     'route_ids': [(4, route.id) for route in values.get('route_ids', [])],
        #     'warehouse_id': self.propagate_warehouse_id.id or self.warehouse_id.id,
        #     'date': date_expected,
        #     'date_expected': date_expected,
        #     'propagate': self.propagate,
        #     'priority': values.get('priority', "1"),



