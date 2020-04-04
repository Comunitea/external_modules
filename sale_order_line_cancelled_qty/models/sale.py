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
    @api.depends('move_ids.state')
    def _compute_qty_pending(self):
        if self.ids:
            if len(self.ids) == 1:
                where = 'sm.sale_line_id = {}'.format(self.id)
            else:
                where = 'sm.sale_line_id in {}'.format(tuple(self.ids))
            sql = "select " \
                  "sale_line_id, sum(sm.product_uom_qty) as qty_ordered " \
                  "from stock_move sm " \
                  "join stock_location sl on sl.id = sm.location_dest_id " \
                  "where sm.state not in ('done', 'cancel', 'draft') and sl.usage = 'customer' and {} group by sm.sale_line_id".format(where)
            self._cr.execute(sql)
            res = self._cr.fetchall()
            for line in res:
                sol = self.filtered(lambda x: x.id == line[0])
                qty_pending = line[1]
                sol.qty_pending = sol.product_uom._compute_quantity(qty_pending, sol.product_uom)

    @api.multi
    def _calculate_cancelled_qty(self):
        if self.ids:
            if len(self.ids) == 1:
                where = 'sm.sale_line_id = {}'.format(self.id)
            else:
                where = 'sm.sale_line_id in {}'.format(tuple(self.ids))
            sql = """
            SELECT SUM(sm.product_uom_qty), sale_line_id
            FROM stock_move sm JOIN stock_location sl
                ON sl.id = sm.location_dest_id
            WHERE sm.origin_returned_move_id IS NULL
                AND sm.state = 'cancel'
                AND sl.usage = 'customer'
                AND {}
             GROUP BY sale_line_id""".format(where)
            self._cr.execute(sql)
            res = self._cr.fetchall()
            for rec in res:
                if rec[0]:
                    qty_cancelled = rec[0]
                    line = self.filtered(lambda l: l.id == rec[1])
                    line.qty_cancelled = line.product_uom._compute_quantity(
                        qty_cancelled, line.product_uom)

    @api.multi
    @api.depends('move_ids.state', 'move_ids.scrapped',
                 'move_ids.product_uom_qty', 'move_ids.product_uom')
    def _compute_qty_delivered(self):
        res = super(SaleOrderLine, self)._compute_qty_delivered()
        self._calculate_cancelled_qty()
        self._compute_qty_pending()
        return res

    qty_cancelled = fields.Float(
        copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        default=0.0)

    qty_pending = fields.Float('Cantidad pendiente', compute_sudo=True,
                               compute='_compute_qty_pending', store=True)
