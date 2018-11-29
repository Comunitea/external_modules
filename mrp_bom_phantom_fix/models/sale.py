# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    has_packs = fields.Boolean(compute='_compute_has_packs')

    @api.depends('order_line.product_id')
    def _compute_has_packs(self):
        for order in self:
            has_packs = False
            for line in self.order_line:
                if line.pack_components:
                    has_packs = True
                    break
            order.has_packs = has_packs


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pack_components = fields.Text(compute='_compute_pack_components')

    @api.multi
    def _get_delivered_qty(self):
        res = super(SaleOrderLine, self)._get_delivered_qty()
        qty = 0
        self.ensure_one()
        bom = self.env['mrp.bom']._bom_find(product=self.product_id)
        if bom and bom.type == 'phantom':
            # Calculamos la cantidad de producto en base a componentes.
            # En caso de incongruencia de cantidades P.E.: 1pack = 5A + 4B
            # cantidades entregadas 8A y 6B. Se establece la cantidad
            # minima de pack.
            moves = self.move_ids.filtered(
                lambda r: r.state == 'done' and not r.scrapped)
            quantities = self._get_bom_component_qty(bom)
            delivered_qties = {}
            returned_qties = {}
            for move in moves:
                quantities_uom = self.env['product.uom'].browse(
                    quantities[move.product_id.id]['uom'])
                pack_qty = move.product_uom._compute_quantity(
                    move.product_uom_qty,
                    quantities_uom)
                if move.location_dest_id.usage == "customer":
                    if not move.origin_returned_move_id or \
                            (move.origin_returned_move_id and move.to_refund):
                        if move.product_id.id not in delivered_qties:
                            delivered_qties[move.product_id.id] = 0.0
                        delivered_qties[move.product_id.id] += pack_qty
                elif move.location_dest_id.usage != "customer" and \
                        move.to_refund:
                    if move.product_id.id not in returned_qties:
                        returned_qties[move.product_id.id] = 0.0
                    returned_qties[move.product_id.id] += pack_qty
                delivered = self.get_pack_quantity(delivered_qties, quantities)
                returned = self.get_pack_quantity(returned_qties, quantities)
                qty = delivered - returned
            res = qty
        return res

    def get_pack_quantity(self, quantities, bom_quantities):
        if not quantities:
            return 0.0
        pack_qty = self.product_uom_qty
        for product_id in quantities.keys():
            qty = quantities[product_id] / bom_quantities[product_id]['qty']
            if qty < pack_qty:
                pack_qty = qty
        return pack_qty

    @api.depends('product_id', 'product_uom_qty')
    def _compute_pack_components(self):
        for line in self:
            pack_components = []
            bom = self.env['mrp.bom']._bom_find(product=line.product_id)
            if bom and bom.type == 'phantom':
                quantities = line._get_bom_component_qty(bom)
                for product_id in quantities.keys():
                    product = self.env['product.product'].browse(product_id)
                    uom = self.env['product.uom'].browse(
                        quantities[product_id]['uom'])
                    pack_components.append(
                        '%s %s %s' % (quantities[product_id]['qty'],
                                      uom.name, product.name))
            line.pack_components = '\n'.join(pack_components)
