# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        domain = [('state', '=','cancel'), ('sale_line_id','in', self.mapped('order_line').ids)]
        moves_to_unlink = self.env['stock.move'].search(domain).filtered(lambda x: x.quantity_done == 0)
        moves_to_unlink.write({'sale_line_id': False})
        return res

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _calculate_cancelled_qty(self):
        for line in self.filtered(lambda r: r.product_id and r.id):
            sql = """
            SELECT SUM(sm.product_uom_qty)
            FROM stock_move sm JOIN stock_location sl
                ON sl.id = sm.location_dest_id
            WHERE sm.origin_returned_move_id IS NULL
                AND sm.state = 'cancel'
                AND sl.usage = 'customer'
                AND sale_line_id = {}""".format(line.id)
            self._cr.execute(sql)
            res = self._cr.fetchall()
            if res[0] and res[0][0]:
                qty_cancelled = res[0][0]
                line.qty_cancelled = line.product_uom._compute_quantity(
                    qty_cancelled, line.product_uom)
            else:
                line.qty_cancelled = 0.0

    def _compute_qty_delivered(self):
        res = super(SaleOrderLine, self)._compute_qty_delivered()
        self._calculate_cancelled_qty()
        return res

    qty_cancelled = fields.Float(
        copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        default=0.0)
