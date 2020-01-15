# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _calculate_cancelled_qty(self):

        if self.ids:
            sql = """
            SELECT SUM(sm.product_uom_qty), sale_line_id
            FROM stock_move sm JOIN stock_location sl
                ON sl.id = sm.location_dest_id
            WHERE sm.origin_returned_move_id IS NULL
                AND sm.state = 'cancel'
                AND sl.usage = 'customer'
                AND sale_line_id in %s
             GROUP BY sale_line_id"""
            print(self.ids)
            self._cr.execute(sql, (tuple(self.ids),))
            res = self._cr.fetchall()
            for rec in res:
                if rec[0]:
                    qty_cancelled = rec[0]
                    line = self.filtered(lambda l: l.id == rec[1])
                    line.qty_cancelled = line.product_uom._compute_quantity(
                        qty_cancelled, line.product_uom)

    def _compute_qty_delivered(self):
        res = super(SaleOrderLine, self)._compute_qty_delivered()
        self._calculate_cancelled_qty()
        return res

    qty_cancelled = fields.Float(
        copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        default=0.0)
