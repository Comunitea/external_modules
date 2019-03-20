# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from operator import itemgetter
from itertools import groupby

class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.depends('group_move_lines')
    def _get_group_picking_ids(self):
        for pick in self:
            pick.group_picking_ids = pick.group_move_lines.mapped("picking_id")


    group_pick = fields.Boolean('Grouped pick')
    group_move_lines = fields.One2many('stock.move', 'group_picking_id', string="Stock Moves", copy=True)
    group_move_line_ids = fields.One2many('stock.move.line', 'group_picking_id', 'Operations')
    group_picking_ids = fields.One2many('stock.picking', compute=_get_group_picking_ids)
    group_move_line_exist = fields.Boolean(
        'Has Pack Operations', compute='_compute_group_move_line_exist',
        help='Check the existence of pack operation on the picking')

    @api.model
    def search(self, args, offset=0, limit=0, order=None, count=False):
        """ Convert the search on real ids in the case it was asked on virtual ids, then call super() """
        assign_pick = self.env.context.get('assign_pick')
        if assign_pick:
            args += []
        return super().search(args, offset=offset, limit=limit,
                              order=order, count=count)

    def _assign_picking(self):
        ctx = self._context.copy()
        ctx.update(assign_picking=True)
        return super(StockPicking, self.with_context(ctx))._assign_picking()


    @api.depends('move_type', 'move_lines.state', 'move_lines.picking_id', 'group_move_lines.state', 'group_move_lines.group_picking_id')
    @api.one
    def _compute_state(self):
        if self.group_pick:
            lines = self.group_move_lines
        else:
            lines = self.move_lines



        if not lines:
            self.state = 'draft'
        elif any(move.state == 'draft' for move in lines):  # TDE FIXME: should be all ?
            self.state = 'draft'
        elif all(move.state == 'cancel' for move in lines):
            self.state = 'cancel'
        elif all(move.state in ['cancel', 'done'] for move in lines):
            self.state = 'done'
        else:
            relevant_move_state = lines._get_relevant_state_among_moves()
            if relevant_move_state == 'partially_available':
                self.state = 'assigned'
            else:
                self.state = relevant_move_state

    @api.one
    @api.depends('move_lines.priority', 'group_move_lines.priority')
    def _compute_priority(self):
        if self.group_pick:
            lines = self.mapped('group_move_lines')
        else:
            lines = self.mapped('move_lines')

        if lines:
            priorities = [priority for priority in lines.mapped('priority') if priority] or ['1']
            self.priority = max(priorities)
        else:
            self.priority = '1'

    @api.one
    @api.depends('move_lines.date_expected', 'group_move_lines.date_expected')
    def _compute_scheduled_date(self):
        if self.group_pick:
            lines = self.group_move_lines
        else:
            lines = self.move_lines
        if self.move_type == 'direct':
            self.scheduled_date = min(lines.mapped('date_expected') or [fields.Datetime.now()])
        else:
            self.scheduled_date = max(lines.mapped('date_expected') or [fields.Datetime.now()])

    @api.one
    def _compute_group_move_line_exist(self):
        self.group_move_line_exists = bool(self.group_move_line_ids)

    @api.multi
    def _compute_show_check_availability(self):

        for picking in self:
            if picking.group_pick:
                lines = picking.group_move_lines
            else:
                lines = picking.move_lines

            has_moves_to_reserve = any(
                move.state in ('waiting', 'confirmed', 'partially_available') and
                float_compare(move.product_uom_qty, 0, precision_rounding=move.product_uom.rounding)
                for move in lines
            )
            picking.show_check_availability = picking.is_locked and picking.state in (
            'confirmed', 'waiting', 'assigned') and has_moves_to_reserve

    @api.multi
    def action_assign(self):

        res = super().action_assign()

        moves = self.mapped('group_move_lines').filtered(lambda move: move.state not in ('draft', 'cancel', 'done'))

        moves._action_assign()

        return res

    @api.multi
    def force_assign(self):

        super().force_assign()
        """ Changes state of picking to available if moves are confirmed or waiting.
        @return: True
        """
        self.mapped('group_move_lines').filtered(
            lambda move: move.state in ['confirmed', 'waiting', 'partially_available'])._force_assign()
        return True

    @api.multi
    def action_cancel(self):

        self.mapped('group_move_lines').write({'group_picking_id': False})
        return super().action_cancel()

    @api.multi
    def action_done(self):
        if not self.group_pick:
            return super().action_done()
        """Changes picking state to done by processing the Stock Moves of the Picking

        Normally that happens when the button "Done" is pressed on a Picking view.
        @return: True
        """
        # TDE FIXME: remove decorator when migration the remaining
        todo_moves = self.mapped('group_move_lines').filtered(
            lambda self: self.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed'])
        # Check if there are ops not linked to moves yet
        for pick in self:
            # # Explode manually added packages
            # for ops in pick.move_line_ids.filtered(lambda x: not x.move_id and not x.product_id):
            #     for quant in ops.package_id.quant_ids: #Or use get_content for multiple levels
            #         self.move_line_ids.create({'product_id': quant.product_id.id,
            #                                    'package_id': quant.package_id.id,
            #                                    'result_package_id': ops.result_package_id,
            #                                    'lot_id': quant.lot_id.id,
            #                                    'owner_id': quant.owner_id.id,
            #                                    'product_uom_id': quant.product_id.uom_id.id,
            #                                    'product_qty': quant.qty,
            #                                    'qty_done': quant.qty,
            #                                    'location_id': quant.location_id.id, # Could be ops too
            #                                    'location_dest_id': ops.location_dest_id.id,
            #                                    'picking_id': pick.id
            #                                    }) # Might change first element
            # # Link existing moves or add moves when no one is related
            for ops in pick.group_move_line_ids.filtered(lambda x: not x.move_id):
                # Search move with this product
                moves = pick.group_move_lines.filtered(lambda x: x.product_id == ops.product_id)
                moves = sorted(moves, key=lambda m: m.quantity_done < m.product_qty, reverse=True)
                if moves:
                    ops.move_id = moves[0].id
                else:
                    new_move = self.env['stock.move'].create({
                        'name': _('New Move:') + ops.product_id.display_name,
                        'product_id': ops.product_id.id,
                        'product_uom_qty': ops.qty_done,
                        'product_uom': ops.product_uom_id.id,
                        'location_id': pick.location_id.id,
                        'location_dest_id': pick.location_dest_id.id,
                        'picking_id': pick.id,
                    })
                    ops.move_id = new_move.id
                    new_move._action_confirm()
                    todo_moves |= new_move
                    # 'qty_done': ops.qty_done})
        todo_moves._action_done()
        self.write({'date_done': fields.Datetime.now()})
        return True


    def _check_move_lines_map_quant_package(self, package):
        if not self.group_pick:
            return super()._check_move_lines_map_quant_package()
        """ This method checks that all product of the package (quant) are well present in the move_line_ids of the picking. """
        all_in = True
        pack_move_lines = self.group_move_line_ids.filtered(lambda ml: ml.package_id == package)
        keys = ['product_id', 'lot_id']
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        grouped_quants = {}
        for k, g in groupby(sorted(package.quant_ids, key=itemgetter(*keys)), key=itemgetter(*keys)):
            grouped_quants[k] = sum(self.env['stock.quant'].concat(*list(g)).mapped('quantity'))

        grouped_ops = {}
        for k, g in groupby(sorted(pack_move_lines, key=itemgetter(*keys)), key=itemgetter(*keys)):
            grouped_ops[k] = sum(self.env['stock.move.line'].concat(*list(g)).mapped('product_qty'))
        if any(not float_is_zero(grouped_quants.get(key, 0) - grouped_ops.get(key, 0), precision_digits=precision_digits) for key in grouped_quants) \
                or any(not float_is_zero(grouped_ops.get(key, 0) - grouped_quants.get(key, 0), precision_digits=precision_digits) for key in grouped_ops):
            all_in = False
        return all_in

    @api.multi
    def _check_entire_pack(self):
        if not self.group_pick:
            super()._check_entire_pack()
        """ This function check if entire packs are moved in the picking"""
        for picking in self:
            origin_packages = picking.group_move_line_ids.mapped("package_id")
            for pack in origin_packages:
                if picking._check_move_lines_map_quant_package(pack):
                    picking.group_move_line_ids.filtered(lambda ml: ml.package_id == pack).write({'result_package_id': pack.id})

    @api.multi
    def do_unreserve(self):

        for picking in self:
            picking.group_move_lines._do_unreserve()
            picking.move_lines._do_unreserve()

