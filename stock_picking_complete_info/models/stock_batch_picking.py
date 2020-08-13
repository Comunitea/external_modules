# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError

class StockBatchPicking(models.Model):
    _inherit = 'stock.picking.batch'

    @api.multi
    def _count_product_ids(self):
        for pick in self:
            count = len(pick.move_lines.mapped('product_id'))
            pick.product_ids_count = count

    reserved_availability = fields.Float(
        'Quantity Reserved', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    quantity_done = fields.Float(
        'Quantity Done', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    product_uom_qty = fields.Float(
        'Quantity', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    product_ids_count = fields.Integer('# Products',
                                       compute='_count_product_ids')
    all_assigned = fields.Boolean('All assigned', compute='get_all_assigned')
    price_subtotal = fields.Float(string='Subtotal', currency_field='currency_id', compute='compute_picking_qties')
    move_lines_count = fields.Integer('# Lines', compute='compute_move_lines_count')
    info_str = fields.Char('Info str', compute='compute_picking_qties')
    n_lines = fields.Char(store=False)
    n_amount = fields.Char(store=False)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type')
    picking_dest_ids = fields.One2many('stock.picking', string='Picking enlazados', compute="compute_picking_qties")
    batch_dest_id = fields.Many2one('stock.picking.batch', string="Dest batch picking")

    @api.multi
    def get_all_assigned(self):
        for pick in self:
            pick.all_assigned = all(x.all_assigned for x in pick.picking_ids)

    @api.multi
    def compute_move_lines_count(self):
        for batch in self:
            batch.move_lines_count = sum(x.move_lines_count for x in batch.picking_ids)

    @api.multi
    def compute_picking_qties(self):
        for batch in self:
            batch.quantity_done = sum(x.quantity_done for x in batch.picking_ids)
            batch.reserved_availability = sum(x.reserved_availability for x in batch.picking_ids)
            batch.product_uom_qty = sum(x.product_uom_qty for x in batch.picking_ids)
            #batch.move_lines_count = sum(x.move_lines_count for x in batch.picking_ids)
            batch.price_subtotal = sum(x.price_subtotal for x in batch.picking_ids)
            batch.info_str = _('{} €: {} lines'.format(batch.price_subtotal, batch.move_lines_count))
            batch.picking_dest_ids = batch.move_lines.mapped('move_dest_ids').mapped('picking_id')

    @api.multi
    def force_set_qty_done(self):
        return self.mapped('picking_ids').force_set_qty_done()
        field = self._context.get('field', 'product_uom_qty')
        reset = self._context.get('reset', True)
        return self.mapped('picking_ids').force_set_qty_done()
        states = ('confirmed', 'assigned')
        for picking in self.mapped('picking_ids').force_set_qty_done():
            if picking.state not in states:
                raise ValidationError(_('State {} incorrect for {}'.format(picking.state, picking.name)))
            picking.move_lines.force_set_qty_done(reset, field)