# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _prepare_quant_ids(self):
        sequence = 10
        if self._context.get('reload', False):
            last_domain = [('quant_id', '=', self.id)]
            last = self.env['unreserved.available.quant'].search_read(last_domain, fields=['sequence'], limit=1,
                                                                    order='id desc')
            sequence = last and last[0]['sequence'] or 10

        vals = {
                'quant_id': self.id,
                'product_id': self.product_id.id,
                'location_id': self.location_id.id,
                'package_id': self.package_id and self.package_id.id or False,
                'lot_id': self.lot_id and self.lot_id.id or False,
                'owner_id': self.owner_id and self.owner_id.id or False,
                'quantity': self.quantity,
                'available_quantity':self.quantity - self.reserved_quantity,
                'reserved_quantity': self.reserved_quantity,
                'sequence': sequence
                }
        return vals

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_change_vals (self):

        package_ids = self.move_line_ids.mapped('result_package_id')
        lot_ids = self.move_line_ids.mapped('lot_id')
        owner_ids = self.move_line_ids.mapped('lot_id')
        sequence = 10
        if self._context.get('reload', False):
            last_domain = [('move_id', '=', self.id)]
            last = self.env['move.change.reserve.line'].search_read(last_domain, fields=['sequence'], limit=1, order='id desc')
            sequence = last and last[0]['sequence'] or 10

        vals =  {'location_id': self.location_id.id,
                'product_uom_qty': self.product_uom_qty,
                'product_uom': self.product_uom.id,
                'reserved_availability': self.reserved_availability,
                'new_reserved_availability': 0.00,
                'partner_id': self.partner_id and self.partner_id.id or False,
                'sale_id': self.sale_line_id and self.sale_line_id.order_id.id or False,
                'origin': self.origin,
                'move_id': self.id,
                'state': self.state,
                'move_str': '{}: {}>{}'.format(self.origin, self.location_id.name, self.location_dest_id.name),
                'date_expected': self.date_expected,
                'package_ids': [(6, 0, package_ids.ids)],
                'lot_ids': [(6, 0, lot_ids.ids)],
                'owner_ids': [(6, 0, owner_ids.ids)],
                'move_id_id': self.id,
                'sequence': sequence
                }
        return vals

    def get_reserved_move_domain(self):
        picking_type_id = self.picking_type_id

        if picking_type_id.default_location_src_id \
                and self.location_id != picking_type_id.default_location_src_id \
                and (picking_type_id.default_location_src_id.child_ids and self.location_id in picking_type_id.default_location_src_id.child_ids):
            location_id = picking_type_id.default_location_src_id
        else:
            location_id = self.location_id
        if location_id in picking_type_id.warehouse_id.lot_stock_id.child_ids:
            location_id = picking_type_id.warehouse_id.lot_stock_id

        if picking_type_id.default_location_dest_id \
                and self.location_dest_id != picking_type_id.default_location_dest_id \
                and (picking_type_id.default_location_dest_id.child_ids and self.location_dest_id in picking_type_id.default_location_dest_id.child_ids):
            location_dest_id = picking_type_id.location_dest_id
        else:
            location_dest_id = self.location_dest_id

        if location_dest_id in picking_type_id.warehouse_id.lot_stock_id.child_ids:
            location_dest_id = picking_type_id.warehouse_id.lot_stock_id

        reserved_move_domain = [
                                ('location_id', 'child_of', location_id.id),
                                ('product_id', '=', self.product_id.id),
                                ('state', 'in', ('confirmed', 'assigned', 'partially_available'))]
        return reserved_move_domain, location_id, location_dest_id

    def default_quant_reorder(self, quants):
        return quants

    def default_moves_reorder(self, moves):
        return moves.sorted(lambda x: (x.id != self.id, x.date_expected))

    def get_move_change_wzd_vals(self):
        get_reserved_move_domain, location_id, location_dest_id = self.get_reserved_move_domain()
        reserved_move_ids = self.default_moves_reorder(self.env['stock.move'].search(get_reserved_move_domain))

        quant_domain = [('location_id', 'child_of', location_id.id),
                        ('product_id', '=', self.product_id.id)]
        ##MUY FEO PERO NO VEO OTRA FORMA
        removal_strategy = self.env['stock.quant']._get_removal_strategy(self.product_id, self.location_id)
        removal_strategy_order = self.env['stock.quant']._get_removal_strategy_order(removal_strategy)
        removal_strategy_order = removal_strategy_order.replace('NULLS','')
        removal_strategy_order = removal_strategy_order.replace('LAST', '')
        removal_strategy_order = removal_strategy_order.replace('FIRST', '')
        quant_ids = self.default_quant_reorder(self.env['stock.quant'].search(quant_domain, order=removal_strategy_order))

        vals = {'move_id': self.id,

                'location_id': location_id.id,
                'location_dest_id': location_dest_id.id,
                'partner_id': self.partner_id and self.partner_id.id or False,
                'sale_id': self.sale_line_id and self.sale_line_id.order_id.id or False,
                'origin': self.origin,
                'product_id': self.product_id.id,
                'state': self.state,
                'move_line_ids': [(6, 0, self.move_line_ids.ids)],
                'reserved_move_ids': [(0, 0, x._prepare_move_change_vals()) for x in reserved_move_ids],
                'quant_ids': [(0, 0, x._prepare_quant_ids()) for x in quant_ids],
                'total_product_uom_qty': sum(x.product_uom_qty for x in reserved_move_ids),
                'total_reserved_availability': sum(x.reserved_availability for x in reserved_move_ids),
                'total_available': sum(x.quantity for x in quant_ids),
                'show_lots_text': self.product_id.tracking != 'none',
                'show_move_packs': any(x.package_id for x in reserved_move_ids.mapped('move_line_ids').mapped('package_id')),
                'show_quant_packs': any(x.package_id for x in quant_ids),
        }
        return vals

    def open_move_change_reserve_wzd(self):
        wzd_vals = self.get_move_change_wzd_vals()
        wzd_id = self.env['move.change.reserve.wzd'].create(wzd_vals)
        action = wzd_id.get_formview_action()
        action['target'] = 'new'
        return action

    def _split(self, qty, restrict_partner_id=False):
        res = super()._split(qty=qty, restrict_partner_id=restrict_partner_id )
        if self.state == 'partially_available':
            precision_digits = self.env[
                'decimal.precision'].precision_get('Product Unit of Measure')
            if float_compare(self.product_uom_qty, self.product_uom_qty, precision_digits=precision_digits) == 0:
                self.write({'state': 'assigned'})
        return res