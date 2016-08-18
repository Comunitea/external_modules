# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from openerp import models, api, fields
import openerp.addons.decimal_precision as dp


class StockTransferDetails(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.model
    def default_get(self, fields):
        """
        Overwrited to get the secondary unit to the item line.
        """
        res = super(StockTransferDetails, self).default_get(fields)

        t_uom = self.env['product.uom']
        picking_ids = self._context.get('active_ids', [])
        if len(picking_ids) != 1:
            return res

        res['item_ids'] = []    # We calc again the item ids
        picking = self.env['stock.picking'].browse(picking_ids[0])

        if not picking.pack_operation_ids:
            picking.do_prepare_partial()

        items = packs = []
        for op in picking.pack_operation_ids:
            uos_id = uom_id = op.product_uom_id.id
            uos_qty = uom_qty = op.product_qty

            if op.linked_move_operation_ids:
                move = op.linked_move_operation_ids[0].move_id
                uos_id = move.product_uos.id or uos_id
                uos_qty = t_uom._compute_qty(uom_id, uom_qty, uos_id)

            item = {
                'packop_id': op.id,
                'product_id': op.product_id.id,
                'product_uom_id': op.product_uom_id.id,
                'quantity': op.product_qty,
                'package_id': op.package_id.id,
                'lot_id': op.lot_id.id,
                'sourceloc_id': op.location_id.id,
                'destinationloc_id': op.location_dest_id.id,
                'result_package_id': op.result_package_id.id,
                'date': op.date,
                'owner_id': op.owner_id.id,
                'uos_qty': uos_qty,  # Calculed and added
                'uos_id': uos_id,     # Calculed and added
            }
            if op.product_id:
                items.append(item)
            elif op.package_id:
                packs.append(item)
        res.update(item_ids=items, pickop_ids=packs)
        return res


class StockTransferDetailsItems(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    uos_qty = fields.Float('Quantity (S.U.)',
                           digits_compute=dp.
                           get_precision('Product Unit of Measure'))
    uos_id = fields.Many2one('product.uom', 'Second Unit', readonly=True)

    @api.onchange('quantity')
    def quantity_onchange(self):
        """
        We change uos_qty field
        """
        t_uom = self.env['product.uom']
        if self.env.context.get("skip_uos_qty_onchange"):
            self.env.context = self.with_context(
                skip_uos_qty_onchange=False).env.context
        else:
            if self.uos_id:
                self.env.context = self.with_context(
                    skip_uos_qty_onchange=True).env.context
                self.uos_qty = t_uom._compute_qty(self.product_uom_id.id,
                                                  self.quantity,
                                                  self.uos_id.id)

    @api.onchange('uos_qty')
    def uos_qty_onchange(self):
        """
        We change quantity field
        """
        t_uom = self.env['product.uom']
        if self.env.context.get("skip_uos_qty_onchange"):
            self.env.context = self.with_context(
                skip_uos_qty_onchange=False).env.context
        else:
            if self.product_uom_id:
                self.env.context = self.with_context(
                    skip_uos_qty_onchange=True).env.context
                self.quantity = t_uom._compute_qty(self.uos_id.id,
                                                   self.uos_qty,
                                                   self.product_uom_id.id)

    @api.multi
    def write(self, vals):
        """
        We change uos_qty field when split_quantities divide the lines
        """
        res = super(StockTransferDetailsItems, self).write(vals)
        if vals.get('quantity'):
            self.quantity_onchange()
        return res
