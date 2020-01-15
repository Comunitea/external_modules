# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def button_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        domain = [('state', '=','cancel'), ('purchase_line_id','in', self.mapped('order_line').ids)]
        moves_to_unlink = self.env['stock.move'].search(domain).filtered(lambda x: x.quantity_done == 0)
        moves_to_unlink.write({'purchase_line_id': False})
        return res

class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    def _calculate_cancelled_qty(self):
        for line in self.filtered(lambda r: r.product_id and r.id):
            sql = """
            SELECT SUM(sm.product_uom_qty)
            FROM stock_move sm
                JOIN stock_location sl ON sl.id = sm.location_id
            WHERE sm.origin_returned_move_id IS NULL
                AND sm.state = 'cancel'
                AND sl.usage = 'supplier'
                AND sm.purchase_line_id = {}""".format(line.id)
            self._cr.execute(sql)
            res = self._cr.fetchall()
            if res and len(res) == 1:
                qty_cancelled = res[0][0] or 0.0
                line.qty_cancelled = line.product_uom._compute_quantity(
                    qty_cancelled, line.product_uom)
            else:
                line.qty_cancelled = 0.0

    def _update_received_qty(self):
        res = super()._update_received_qty()
        self._calculate_cancelled_qty()
        return res

    qty_cancelled = fields.Float(
        copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        default=0.0)


