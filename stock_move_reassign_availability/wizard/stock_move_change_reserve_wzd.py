# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare



class StockQuant(models.Model):

    _inherit ='stock.quant'

    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        return super()._gather(product_id=product_id, location_id=location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict)

class UnreservedAvailableQuant(models.TransientModel):
    _name ="unreserved.available.quant"

    wzd_id = fields.Many2one('move.change.reserve.wzd')
    quant_id = fields.Many2one('stock.quant', 'Quant')
    sequence = fields.Integer('Order when re-reserve')
    location_id = fields.Many2one('stock.location', 'Location')
    package_id = fields.Many2one('stock.quant.package', 'Package')
    lot_id = fields.Many2one('stock.production.lot', 'Lot')
    owner_id = fields.Many2one('res.partner', 'Owner', help="Owner of the quants")
    move_str = fields.Char()
    quantity = fields.Float(
        'Available quantity',
        digits=dp.get_precision('Product Unit of Measure'))

    product_uom = fields.Many2one('product.uom', 'Unit of Measure')
    reserved_quantity = fields.Float(
        'Quantity Reserved', digits=dp.get_precision('Product Unit of Measure'),
        help='Quantity that has already been reserved for this move')
    available_quantity = fields.Float(
        'Quantity Available', digits=dp.get_precision('Product Unit of Measure'),
        help='Quantity that has already been reserved for this move')
    state = fields.Char()

class MoveChangeReserveLine(models.TransientModel):
    _name = 'move.change.reserve.line'

    wzd_id = fields.Many2one('move.change.reserve.wzd')
    quant_id = fields.Many2one('stock.quant', 'Quant')
    sequence = fields.Integer('Order when re-reserve')
    location_id = fields.Many2one('stock.location', 'Location')
    location_dest_id = fields.Many2one('stock.location', string='Location')
    package_ids = fields.Many2many('stock.quant.package', string='Package')
    lot_ids = fields.Many2many('stock.production.lot',  string='Lot')
    owner_ids = fields.Many2many('res.partner', string='Owner', help="Owner of the quants")
    move_str = fields.Char()
    product_uom_qty = fields.Float(
        'Initial Demand',
        digits=dp.get_precision('Product Unit of Measure'), help="This is the quantity of products from an inventory "
             "point of view. For moves in the state 'done', this is the "
             "quantity of products that were actually moved. For other "
             "moves, this is the quantity of product that is planned to "
             "be moved. Lowering this quantity does not generate a "
             "backorder. Changing this quantity on assigned moves affects "
             "the product reservation, and should be done with care.")

    product_uom = fields.Many2one('product.uom', 'Unit of Measure')
    reserved_availability = fields.Float(
        'Quantity Reserved', digits=dp.get_precision('Product Unit of Measure'),
        readonly=True, help='Quantity that has already been reserved for this move')
    new_reserved_availability = fields.Float(
        'New Quantity To Reseve', digits=dp.get_precision('Product Unit of Measure'),

        readonly=True, help='Quantity that will be reserved for this move')
    quantity_to_split = fields.Float(
        'Quantity To spit', digits=dp.get_precision('Product Unit of Measure'))
    partner_id = fields.Many2one('res.partner', 'Partner')
    sale_id = fields.Many2one('sale.order', 'Sale Order')
    origin = fields.Char("Source Document")
    state = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')], string='Status',)
    move_id = fields.Many2one('stock.move')
    date_expected = fields.Datetime(
        'Expected Date')
    move_id_id = fields.Integer()


    def get_move_values(self, move_id, quant_id, picking_type_id):
        vals = {
            'location_id': quant_id.location_id.id,
            'picking_type_id': picking_type_id.id,
            'picking_id': False
        }
        return vals

    def after_update(self, move):
        return True

    def get_picking_domain(self, move_id, quant):
        domain = [('default_location_src_id', '=', quant.location_id.id),
                              ('code', '=', move_id.picking_type_id.code),
                              ('default_location_dest_id', '=', move_id.location_dest_id.id)]

        return domain

    def update_reserved_quantity(self, move, quant, new_reserved_availability):
        precision_digits = self.env[
            'decimal.precision'].precision_get('Product Unit of Measure')
        available_quantity = 0.0
        if float_compare(new_reserved_availability, 0.0, precision_digits=precision_digits) > 0:
            available_quantity = quant._get_available_quantity(
                move.product_id, quant.location_id, lot_id=quant.lot_id,
                package_id=quant.package_id, owner_id=quant.owner_id,
            )
        if float_compare(
                available_quantity, 0.0, precision_digits=precision_digits) <= 0:
            return
        move._update_reserved_quantity(
            new_reserved_availability, available_quantity, quant.location_id,
            lot_id=quant.lot_id, package_id=quant.package_id,
            owner_id=quant.owner_id, strict=True
        )
    @api.multi
    def do_reserve(self):
        self.ensure_one()
        moves = self.env['stock.move']
        move_id = self.move_id
        if move_id.state == 'waiting':
            raise ValidationError (_('Move is waiting, you must validate previous move'))
        if move_id.state == 'assigned':
            raise ValidationError (_('Move is asigned, please unreserve to change asigned stock'))

        quants = self.wzd_id.quant_ids.filtered(lambda x: x.available_quantity>0).sorted(key=lambda l: l.sequence)
        quant = quants and quants[0]

        need_qty = move_id.product_uom_qty - move_id.reserved_availability
        if move_id.location_id != quant.location_id:
            new_picking_type_id = self.env['stock.picking.type'].search(self.get_picking_domain(move_id, quant), limit=1)
            if move_id.picking_type_id != new_picking_type_id:
                ## To INHERIT
                if move_id.reserved_availability > 0.00:
                    av_qty = quant.available_quantity
                    if av_qty >= need_qty:
                        split_qty = need_qty
                    else:
                        split_qty = av_qty
                    move_id = self.env['stock.move'].browse(move_id._split(split_qty))
                new_vals = self.get_move_values(move_id=move_id, quant_id=quant, picking_type_id=new_picking_type_id)
                if new_vals:
                    move_id.write(new_vals)
                self.after_update(move_id)
        self.update_reserved_quantity(move_id, quant.quant_id, move_id.product_uom_qty)
        move_id._action_assign()
        move_id.assign_picking()


    @api.multi
    def to_split(self):
        self.ensure_one()
        move_ids = self.env['stock.move']
        for line in self.filtered(lambda x: x.quantity_to_split > 0.00):
            move_id = line.move_id._split(line.quantity_to_split)
            move_ids |= self.env['stock.move'].browse(move_id)
        return self.wzd_id.autorefresh(move_ids)

    @api.multi
    def button_re_reserve_move(self):

        self.ensure_one()
        to_reserve = self.filtered(lambda x: x.state in ('confirmed', 'partially_available')).sorted(key=lambda l: l.sequence)
        for line in to_reserve:
            line.do_reserve()
        move_ids = self.mapped('move_id')
        return self.wzd_id.autorefresh(move_ids)

    @api.multi
    def button_un_reserve_move(self):

        self.ensure_one()
        to_unreserve = self.filtered(lambda x:x.state in ('assigned', 'partially_available')).sorted(key=lambda l: l.sequence)
        for line in to_unreserve:
            line.move_id._do_unreserve()
        move_ids = self.mapped('move_id')
        return self.wzd_id.autorefresh(move_ids)

class MoveChangeQuantWzd(models.TransientModel):
    """Create a stock.batch.picking from stock.picking
    """

    _name = 'move.change.reserve.wzd'
    _description = 'Asistente para cambiar las reservas de almacén'
    _order = 'sequence'

    move_id = fields.Many2one('stock.move', 'Stock move', readonly=1)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=1)
    location_id = fields.Many2one('stock.location', 'Src. Location')
    location_dest_id = fields.Many2one('stock.location', 'Dest. Location')
    sale_id = fields.Many2one('sale.order', 'Sale Order', readonly=1)
    product_id = fields.Many2one(related='move_id.product_id')
    state = fields.Selection(related="move_id.state")
    move_line_ids = fields.One2many(related="move_id.move_line_ids", string='Stock seleccionado')
    reserved_move_ids = fields.One2many('move.change.reserve.line', 'wzd_id', string='Reserved Moves')
    quant_ids = fields.One2many('unreserved.available.quant',  'wzd_id', string="Unreserved stocks")
    origin = fields.Char("Source Document")
    total_product_uom_qty = fields.Float(
        'Total Demand',
        digits=dp.get_precision('Product Unit of Measure'))
    total_reserved_availability = fields.Float(
        'Total Reserved',
        digits=dp.get_precision('Product Unit of Measure'))
    total_available= fields.Float(
        'Total Available',
        digits=dp.get_precision('Product Unit of Measure'))
    show_lots_text = fields.Boolean('Show lots')
    show_move_packs = fields.Boolean('Show move packs')
    show_quant_packs = fields.Boolean('Show quant packs')

    def autorefresh(self, move_ids):
        if not move_ids:
            return
        if len(move_ids) == 1:
            wzd_vals = self.move_id.get_move_change_wzd_vals()
            wzd_id = self.env['move.change.reserve.wzd'].create(wzd_vals)
            action = self.env.ref('stock_move_reassign_availability.action_stock_move_change_reserve_wzd_form').read()[0]
            action['res_id'] = wzd_id.id
        else:
            action = self.env.ref('stock.stock_move_action').read()[0]
            action['domain'] = [('id', 'in', move_ids.ids)]
        action['context'] ={'reload': True}## self._context.copy().update(reload=True)
        return action

    def change_reserve_wzd(self):
        to_reserve = self.reserved_move_ids.filtered(lambda x: x.reserved_availability == 0.00).sorted(key=lambda l: l.sequence)
        to_unreserve = self.reserved_move_ids.filtered(lambda x: x.reserved_availability > 0.00).sorted(key=lambda l: l.sequence)
        for line in to_unreserve:
            line.move_id._do_unreserve()
        for line in to_reserve:
            line.do_reserve()
        return self.wzd_id.autorefresh(self.move_id)


    def action_apply_quant(self):
        return
        quant_ids = self.reserved_move_ids.filtered(lambda x: x.new_quantity>0.00)
        if not quant_ids:
            return
        precision_digits = self.env[
            'decimal.precision'].precision_get('Product Unit of Measure')
        self.move_id._do_unreserve()()
        route_vals = self.move_id.update_info_route_vals()
        moves = self.env['stock.move']
        quant_id = quant_ids[0]

        quant = quant_id.quant_id
        ##SI CAMBIA EL PICKING_TYPE_ID DEL MOVMIMIENTOS SEGÚN LA NUEVA UBICACION
        if self.move_id.picking_type_id.code == 'incoming':
            field = 'location_dest_id'
        else:
            field = 'location_id'

        new_location = quant.location_id

        if new_location.picking_type_id and new_location.picking_type_id != self.move_id.location_id.picking_type_id:
            new_move_id = self.move_id._split(quant_id.new_quantity)
            new_move = self.env['stock.move'].browse(new_move_id)
            ##tengo que cambiarlod e albarán
            new_loc_vals = {
                field: new_location.id,
                'picking_type_id': new_location.picking_type_id.id,
                'picking_id': False
            }
            new_loc_vals.update(route_vals)
            new_move.write(new_loc_vals)
            new_move.check_new_location()
            if float_compare(quant_id.new_quantity, 0.0, precision_digits=precision_digits) > 0:
                available_quantity = quant._get_available_quantity(
                new_move.product_id, quant[field], lot_id=quant.lot_id,
                package_id=quant.package_id, owner_id=quant.owner_id,
                )
            if float_compare(
                available_quantity, 0.0, precision_digits=precision_digits) <= 0:
                return
            new_move._update_reserved_quantity(
                quant_id.new_quantity, available_quantity, quant[field],
                lot_id=quant.lot_id, package_id=quant.package_id,
                owner_id=quant.owner_id, strict=True
            )
            moves |= new_move
        else:
            if float_compare(quant_id.new_quantity, 0.0, precision_digits=precision_digits) > 0:
                available_quantity = quant._get_available_quantity(
                move_id.product_id, quant[field], lot_id=quant.lot_id,
                package_id=quant.package_id, owner_id=quant.owner_id,
                )
            if float_compare(
                available_quantity, 0.0, precision_digits=precision_digits) <= 0:
                return
            move_id._update_reserved_quantity(
                quant_id.new_quantity, available_quantity, quant[field],
                lot_id=quant.lot_id, package_id=quant.package_id,
                owner_id=quant.owner_id, strict=True
            )
            moves |= move_id
        if moves and self.move_id not in moves:
            self.move_id.action_cancel_for_pda()

        moves._action_assign()
        moves.move_sel_assign_picking()
        return self.env['stock.picking.type'].return_action_show_moves(domain=[('id', 'in', moves.ids)])



