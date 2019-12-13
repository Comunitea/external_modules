# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare



class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.multi
    def force_assigned_qty_done(self, reset=True, field='product_uom_qty'):
        if field == 'quantity_done':
            field = 'qty_done'
        elif field == 'reserved_availability':
            field = 'product_uom_qty'
        if reset:
            self.filtered(lambda x: x.qty_done > 0 and x.state != 'done').write({'qty_done': 0})
        else:
            for move in self.filtered(lambda x: not x.qty_done):
                move.qty_done = move[field]


class StockMove(models.Model):
    _inherit = 'stock.move'

    price_subtotal = fields.Monetary(related='sale_line_id.price_subtotal', string='Subtotal', readonly=True)
    currency_id = fields.Many2one(related='sale_line_id.currency_id')

    @api.multi
    def force_set_qty_done(self, reset=True, field='product_uom_qty'):
        for move in self.filtered(lambda x: x.state in ('confirmed', 'assigned', 'partially_available')):
            if move.move_line_ids:
                move.move_line_ids.force_assigned_qty_done(reset, field)
            else:
                move.quantity_done = not reset and move[field] or 0.0

    def _prepare_procurement_values(self):
        res = super(StockMove, self). \
            _prepare_procurement_values()
        res.update({
            'sale_line_id':
                self.sale_line_id.id,
        })
        return res