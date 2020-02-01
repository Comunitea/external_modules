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

    price_subtotal = fields.Monetary(string='Subtotal', currency_field='currency_id', compute='get_price_subtotal')
    price_subtotal_pending = fields.Monetary(string='Subtotal', currency_field='currency_id', compute='get_price_subtotal')
    price_subtotal_reserved = fields.Monetary(string='Subtotal', currency_field='currency_id',
                                             compute='get_price_subtotal')
    currency_id = fields.Many2one('res.currency', compute='get_price_subtotal')

    @api.multi
    def get_price_subtotal(self):
        for move in self:
            prec = 2
            qty = 0
            pending_qty = 0
            reserved_qty = 0
            price_subtotal = 0
            if move.state == 'done':
                reserved_qty = qty = move.quantity_done
                pending_qty = 0
            elif move.state == 'cancel':
                qty = 0
                reserved_qty = 0
                pending_qty = 0
            elif move.state in ('confirmed', 'partially_available', 'assigned'):
                pending_qty = move.product_uom_qty - move.reserved_availability
                qty = move.product_uom_qty
                reserved_qty = move.reserved_availability

            if move.picking_type_id.code != 'incoming':
                sale_line_id = move.sale_line_id or move.move_dest_ids.mapped('sale_line_id')
                if not sale_line_id:
                    sale_id = move.picking_id.sale_id
                    if sale_id:
                        sale_line_id = sale_id.mapped('order_line').filtered(lambda x: x.product_id == move.product_id)

                if sale_line_id and len(sale_line_id) == 1:
                    price = sale_line_id.price_unit * (1 - (sale_line_id.discount or 0.0) / 100.0)

                    # taxes = sale_line_id.tax_id.compute_all(price,
                    #                 sale_line_id.order_id.currency_id, qty,
                    #                 product=sale_line_id.product_id,
                    #                 partner=sale_line_id.order_id.partner_shipping_id)

                    currency_id = sale_line_id.currency_id
                    prec = currency_id.decimal_places
                    price_subtotal = round(qty * price, prec)
                    currency_id = sale_line_id.currency_id
                    line = sale_line_id
                else:
                    price = 0
                    currency_id = False
                    line = False
            else:
                purchase_line_id = move.purchase_line_id
                price = purchase_line_id.price_unit * (1 - (purchase_line_id.discount or 0.0) / 100.0)
                currency_id = purchase_line_id.currency_id
                prec = currency_id.decimal_places
                line = purchase_line_id
                price_subtotal = round(qty * price, prec)

            move.price_subtotal = price_subtotal
            move.price_subtotal_pending = round(pending_qty * price, prec)
            move.price_subtotal_reserved = round(reserved_qty * price, prec)

            move.currency_id = currency_id



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
