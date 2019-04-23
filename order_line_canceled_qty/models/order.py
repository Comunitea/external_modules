# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_cancel(self):
        super().button_cancel(self)
        #self.filtered(lambda x:x.state == "cancel").mapped('order_line').mapped('move_ids').write({'purchase_line_id': False})

class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.multi
    def _get_cancelled_qty(self):
        for line in self:
            if line.product_id and line.id:
                sql = "select SUM(sm.ordered_qty) from stock_move sm " \
                      "join stock_location sl on sl.id = sm.location_dest_id " \
                      "where sm.origin_returned_move_id isnull and sm.state = 'cancel' and sl.usage = 'supplier' and sm.purchase_line_id = {}".format(line.id)
                self._cr.execute(sql)
                res = self._cr.fetchall()
                if res and len(res) == 1:
                    qty_cancelled = res[0][0] or 0.0
                    line.qty_cancelled = line.product_uom._compute_quantity(qty_cancelled, line.product_uom)
                else:
                    line.qty_cancelled = 0.0


    @api.depends('order_id.state', 'move_ids.state', 'move_ids.product_uom_qty')
    def _compute_qty_received(self):
        res = super()._compute_qty_received()
        self._get_cancelled_qty()
        return res

    qty_cancelled = fields.Float(string='Qty cancelled', copy=False, digits=dp.get_precision('Product Unit of Measure'), default=0.0)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        #self.mapped('order_line').mapped('move_ids').write({'sale_line_id': False})
        return res


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _get_cancelled_qty(self):
        for line in self:
            if line.product_id:
                sql = "select SUM(ordered_qty) from stock_move sm " \
                      "join stock_location sl on sl.id = sm.location_dest_id " \
                      "where sm.origin_returned_move_id isnull and sm.state = 'cancel' and sl.usage = 'customer' and sale_line_id = {}".format(line.id)
                self._cr.execute(sql)
                res = self._cr.fetchall()
                if res:
                    qty_cancelled = res[0][0]
                    line.qty_cancelled = line.product_uom._compute_quantity(qty_cancelled, line.product_uom)
                else:
                    line.qty_cancelled = 0.0

    @api.multi
    def _get_delivered_qty(self):
        res = super(SaleOrderLine, self)._get_delivered_qty()
        self._get_cancelled_qty()
        return res

    qty_cancelled = fields.Float(string='Qty cancelled', copy=False, digits=dp.get_precision('Product Unit of Measure'), default=0.0)