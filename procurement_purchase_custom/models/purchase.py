from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_categ_id = fields.Many2one(
        "product.category", string="Category", related="product_id.categ_id"
    )
    to_deliver_qty = fields.Float(compute="_compute_to_deliver_qty")

    def _compute_to_deliver_qty(self):
        # Todo: review
        domain = [
            ('location_id.usage', '=', 'internal'),
            ('location_dest_id.usage', '!=', 'internal'),
            ('state', 'in', ('partially_available', 'assigned', 'confirmed')),
            ('product_id', 'in', self.mapped('product_id').ids)]

        if self._context.get('location'):
            domain += [
                ('location_id', 'child_of', self._context.get('location'))
            ]

        res = self.env['stock.move'].read_group(
            domain, ['product_uom_qty'], ['product_id']
        )
        qties = {}
        for x in res:
            qties[x['product_id'][0]] = x['product_uom_qty']

        for line in self:
            product_id = line.product_id.id
            if product_id in qties.keys():
                line.to_deliver_qty = qties[line.product_id.id]
            else:
                line.to_deliver_qty = 0
        return
