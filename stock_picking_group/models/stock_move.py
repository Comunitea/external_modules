# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

DOMAIN_NOT_STATE = ['draft', 'cancel']

class StockMove(models.Model):

    _inherit = "stock.move"

    sale_id = fields.Many2one('sale.order', 'Saler Order')
    purchase_id = fields.Many2one('purchase.order', 'Purchase Order')
    sale_price = fields.Float('Sale Price')



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
        ctx.update(force_assign=force)
        return self.with_context(ctx)._assign_picking()

    def get_moves_to_not_asign(self):
        to_pick = self.filtered(lambda x: x.sale_id and not x.picking_type_id.grouped)
        not_to_pick = self - to_pick
        return not_to_pick, to_pick

    def check_assign_picking_error(self):
        """
        En caso de asignación en lote se realizan una serie de comprobaciones
        1 - si es de tipo clientes, todos los albaranes tienen el mismo cliente
        2 - si es de tipo proveedor, todos los albaranes tienen el mismo proveedor
        """
        picking_type_id = self.mapped('picking_type_id')
        if len(picking_type_id) > 1:
            raise ValidationError (_('Not same picking types: {}'.format(picking_type_id.mapped("code"))))

        if picking_type_id.code == 'outgoing' :
            if len(self.mapped('partner_id')) > 1:
                raise ValidationError(_('Not same partner for outgoing moves: {}'.format(self.mapped('partner_id').mapped('name'))))

        if picking_type_id.code == 'incoming' :
            if len(self.mapped('partner_id')) > 1:
                raise ValidationError(_('Not same partner for incoming moves: {}'.format(self.mapped('partner_id').mapped('name'))))

        return True


    def get_batch_domain(self):
        self.ensure_one()
        domain = [('state', 'not in', ('draft', 'done', 'cancel')),
                  ('picking_type_id', '=', self.picking_type_id.id)]

        for field in self.picking_type_id.grouped_batch_field_ids:
            if self[field.name]:
                if field.ttype == 'many2one':
                    domain += [(field.name, '=', self[field.name].id)]
                else:
                    domain += [(field.name, '=', self[field.name])]
        return domain

    def get_batch_vals(self):
        vals = {
                'picking_type_id': self.picking_type_id.id,
                'date': self.date_expected,
                }
        for field in self.picking_type_id.grouped_batch_field_ids:
            if self[field.name]:
                if field.ttype == 'many2one':
                    vals.update({field.name: self[field.name].id})
                else:
                    vals.update({field.name: self[field.name]})

        return vals


    def _assign_picking(self):
        self = self.filtered(lambda x: not x.picking_type_id.after_assign)
        self.check_assign_picking_error()
        super()._assign_picking()
        for move in self:
            move.move_line_ids.write({'picking_id': move.picking_id.id})
        return True

    def _get_new_picking_domain(self):
        domain = super()._get_new_picking_domain()

        if self._context.get('pick_domain', False):
            domain += self._context['pick_domain']
        for field in self.picking_type_id.grouped_field_ids:
            if field.ttype == 'many2one':
                domain += [(field.name, '=', self[field.name].id)]
            else:
                domain += [(field.name, '=', self[field.name])]
        return domain

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        for field in self.picking_type_id.grouped_field_ids:
            if field.ttype == 'many2one':
                vals.update({field.name: self[field.name].id})
            else:
                vals.update({field.name: self[field.name]})
        return vals

    def _prepare_move_split_vals(self, qty):
        vals = super()._prepare_move_split_vals(qty)
        if self._context.get('default_location_id', False):
            vals.update(location_id=self['location_id'].id)

        if self._context.get('default_location_dest_id', False):
            vals.update(location_id=self['location_dest_id'].id)

        return vals

    def get_new_location_vals(self, location_field, location):

        vals = {location_field: location._get_location_type_id().id}
        if location.picking_type_id:
            vals.update(picking_type_id = location.picking_type_id.id)
        return vals

    def check_new_location(self, location='location_id'):
        ##COMPRUBA Y ESTABLECE LA NUEVA UBICACIÓN DE ORIGEN DEL MOVIMIENTO Y CAMBIA EL PICKING_TYPE EN CONSECUENCIA. ADEMAS LO SACA DE UN ALBARÁN SI LO TUVIERA
        ##REVISAR BIEN
        if not self.move_line_ids:
            return
        #if not self.picking_type_id.grouped:
        #    return


        default_picking_type_id = self.picking_type_id
        #if not default_picking_type_id.check_sub_locs:
        #    return
        #saco las posibles ubicaciones con albaran de las operaciones
        new_mov_locs = [line[location]._get_location_type_id() for line in self.move_line_ids]
        #print ('Ubicaciones de las operaciones: {} en relación a las que tienen albaranes {}'.format(self.move_line_ids.mapped(location), new_mov_locs))
        # Si solo hay una, la nueva ubicación del movimiento es la de la operación
        if len(new_mov_locs) == 1:
            if new_mov_locs[0] != self[location]:
                vals = self.get_new_location_vals(location, new_mov_locs[0])
                #print("Actualizo el movimiento con vals y reseteo picking_id si lo tuviera")
                self.write(vals)
                self.move_line_ids.write({'picking_id': False})

        elif new_mov_locs:
            ##TODO HAY QUE REVISAR ESTO
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
        if self.picking_id and self.picking_type_id != self.picking_id.picking_type_id:
            self.picking_id = False
            self._assign_picking()

    def _prepare_procurement_values(self):
        """
        Pass move custom fields to the linked move
        """
        vals = super()._prepare_procurement_values()
        vals.update({
            'sale_id': self.sale_id.id,
            'sale_price': self.sale_price,
        })
        return vals

    def _action_assign(self):
        super()._action_assign()
        for move in self.filtered(lambda x: x.location_id.picking_type_id and x.move_line_ids and x.quantity_done == 0):
            move.check_new_location()

    def _action_cancel(self):

        if self._context.get('cancel_from_sale', False):
            new_self = self.filtered(lambda x: x.sale_id == self._context['cancel_from_sale'])
            return super(StockMove, new_self)._action_cancel()

        return super()._action_cancel()

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

        vals.update({
            'sale_price': values.get('sale_price'),
            'sale_id': values.get('sale_id'),

        })
        return vals
