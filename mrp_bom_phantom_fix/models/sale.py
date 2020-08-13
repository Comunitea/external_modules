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
            for line in order.order_line:
                if line.pack_components:
                    has_packs = True
                    break
            order.has_packs = has_packs


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pack_components = fields.Text(compute='_compute_pack_components')

    @api.model
    def _get_bom_component_qty_wt_line(self, product, product_uom, bom):
        bom_quantity = product_uom._compute_quantity(1, bom.product_uom_id)
        boms, lines = bom.explode(product, bom_quantity)
        components = {}
        for line, line_data in lines:
            product = line.product_id.id
            uom = line.product_uom_id
            qty = line.product_qty
            if components.get(product, False):
                if uom.id != components[product]['uom']:
                    from_uom = uom
                    to_uom = self.env['uom.uom'].browse(components[product]['uom'])
                    qty = from_uom._compute_quantity(qty, to_uom)
                components[product]['qty'] += qty
            else:
                # To be in the uom reference of the product
                to_uom = self.env['product.product'].browse(product).uom_id
                if uom.id != to_uom.id:
                    from_uom = uom
                    qty = from_uom._compute_quantity(qty, to_uom)
                components[product] = {'qty': qty, 'uom': to_uom.id}
        return components

    def _compute_margin(self, order_id, product_id, product_uom_id):
        bom = self.env['mrp.bom']._bom_find(product=product_id)
        if bom and bom.type == 'phantom':
            pack_price = 0.0
            quantities = self._get_bom_component_qty_wt_line(product_id, product_uom_id, bom)
            for product_id in quantities.keys():
                pack_product = self.env['product.product'].browse(product_id)
                frm_cur = self.env.user.company_id.currency_id
                to_cur = order_id.pricelist_id.currency_id
                purchase_price = pack_product.standard_price
                if product_uom_id != pack_product.uom_id:
                    purchase_price = pack_product.uom_id._compute_price(purchase_price, product_uom_id)
                price = frm_cur._convert(
                    purchase_price, to_cur, order_id.company_id or self.env.user.company_id,
                    order_id.date_order or fields.Date.today(), round=False)
                pack_price += price * quantities[product_id]['qty']
            return pack_price
        return super()._compute_margin(order_id, product_id, product_uom_id)

    @api.multi
    def _compute_qty_delivered(self):
        res = super()._compute_qty_delivered()
        qty = 0
        for line in self.filtered('product_id'):
            bom = self.env['mrp.bom']._bom_find(product=line.product_id)
            if bom and bom.type == 'phantom':
                # Calculamos la cantidad de producto en base a componentes.
                # En caso de incongruencia de cantidades P.E.: 1pack = 5A + 4B
                # cantidades entregadas 8A y 6B. Se establece la cantidad
                # minima de pack.
                moves = line.move_ids.filtered(
                    lambda r: r.state == 'done' and not r.scrapped)
                quantities = line._get_bom_component_qty(bom)
                delivered_qties = {}
                returned_qties = {}
                for move in moves:
                    quantities_uom = line.env['uom.uom'].browse(
                        quantities[move.product_id.id]['uom'])
                    pack_qty = move.product_uom._compute_quantity(
                        move.product_uom_qty,
                        quantities_uom)
                    if move.location_dest_id.usage == "customer":
                        if not move.origin_returned_move_id or \
                                (move.origin_returned_move_id and
                                 move.to_refund):
                            if move.product_id.id not in delivered_qties:
                                delivered_qties[move.product_id.id] = 0.0
                            delivered_qties[move.product_id.id] += pack_qty
                    elif move.location_dest_id.usage != "customer" and \
                            move.to_refund:
                        if move.product_id.id not in returned_qties:
                            returned_qties[move.product_id.id] = 0.0
                        returned_qties[move.product_id.id] += pack_qty
                    delivered = line.get_pack_quantity(
                        delivered_qties, quantities)
                    returned = line.get_pack_quantity(
                        returned_qties, quantities)
                    qty = delivered - returned
                line.qty_delivered = qty
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
                    uom = self.env['uom.uom'].browse(
                        quantities[product_id]['uom'])
                    pack_components.append(
                        '%s %s %s' % (quantities[product_id]['qty'],
                                      uom.name, product.name))
            line.pack_components = '\n'.join(pack_components)
