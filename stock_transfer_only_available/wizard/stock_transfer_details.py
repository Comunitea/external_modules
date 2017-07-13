# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, api, exceptions, _
from openerp.tools.float_utils import float_compare


class StockTransferDetails(models.TransientModel):

    _inherit = 'stock.transfer_details'

    @api.one
    def do_detailed_transfer(self):
        picking = self.picking_id
        location_obj = self.env['stock.location']
        stock_loc_id = picking.picking_type_id.warehouse_id.lot_stock_id.id
        totals = {}
        for line in self.item_ids:
            if line.product_id.type == 'product':
                if line.sourceloc_id.id not in location_obj.search(
                        [('id', 'child_of', stock_loc_id)])._ids:
                    continue
                if line.product_id.id not in totals:
                    totals[line.product_id.id] = {}
                if line.lot_id.id not in totals[line.product_id.id]:
                    totals[line.product_id.id][line.lot_id.id] = {}
                if line.sourceloc_id.id not in \
                        totals[line.product_id.id][line.lot_id.id]:
                    totals[line.product_id.id][line.lot_id.id][line.sourceloc_id.id] = 0.0
                line_qty_uom = self.env['product.uom']._compute_qty(
                    line.product_uom_id.id, line.quantity,
                    line.product_id.uom_id.id)
                totals[line.product_id.id][line.lot_id.id][line.sourceloc_id.id] += line_qty_uom
        for product in self.env['product.product'].browse(totals.keys()):
            for lot in totals[product.id].keys():
                for location in location_obj.browse(
                        totals[product.id][lot].keys()):

                    quant_vals = [('product_id', '=', product.id),
                                  ('lot_id', '=', lot),
                                  ('location_id', '=', location.id),
                                  '|', ('reservation_id.picking_id', '=',
                                        picking.id),
                                  ('reservation_id', '=', False)]
                    quants = self.env['stock.quant'].search(quant_vals)
                    total_qty = sum([x['qty'] for x in quants.read(['qty'])])
                    difference = float_compare(
                        total_qty, totals[product.id][lot][location.id],
                        precision_rounding=product.uom_id.rounding)
                    if difference < 0:
                        error_message = _(
                            'Not found enought stock in %s for product %s') % \
                                (location.name, product.name)
                        if lot:
                            error_message += _(' with lot %s') % \
                                self.env['stock.production.lot'].browse(
                                lot).name
                        raise exceptions.Warning(
                            _('Quantity error'),
                            error_message
                            )
        return super(StockTransferDetails, self).do_detailed_transfer()
