# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models, fields
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    coupon_code = fields.Char('Promo Coupon Code')

    def clear_existing_promotion_lines(self):
        """
        Deletes existing promotion lines before applying
        @param cursor: Database Cursor
        @param user: ID of User
        @param order: Sale order id
        @param context: Context(no direct use).
        """
        self.ensure_one()
        order = self
        order_line_obj = self.env['sale.order.line']
        # Delete all promotion lines
        domain = [('order_id', '=', order.id), ('promotion_line', '=', True)]
        order_line_objs = order_line_obj.search(domain)

        if order_line_objs:
            order_line_objs.unlink()

        # Clear discount column
        domain = [('order_id', '=', order.id)]
        order_line_objs = order_line_obj.search(domain)
        for line in order_line_objs:
            if line.orig_qty:
                line.write({'product_uom_qty': line.orig_qty})
            if line.old_discount:
                line.write({'discount': line.old_discount,
                            'old_discount': 0.00})

    def apply_commercial_rules(self):
        """
        Applies the promotions to the given records
        @param cursor: Database Cursor
        @param user: ID of User
        @param ids: ID of current record.
        @param context: Context(no direct use).
        """
        promotions_obj = self.env['promos.rules']
        for order in self:
            order.clear_existing_promotion_lines()
            promotions_obj.apply_promotions(order.id)

        return True

    @api.multi
    def copy(self, default=None):
        """
        No duplicar lineas de promoción.
        """
        self.ensure_one()
        res = super(SaleOrder, self).copy(default)
        promo_lines = res.order_line.filtered('promotion_line')
        promo_lines.unlink()
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    promotion_line = fields.Boolean("Rule Line",
                                    help="Indicates if the line was \
                                          created by comemrcial rules")
    orig_qty = fields.Float('Original qty')
    old_discount = fields.Float('Old discount',
                                digits=dp.get_precision('Discount'),
                                default=0.0)
    orig_line_ids = fields.Many2many('sale.order.line',
                                     'line_promo_line_rel',
                                     'line_id1',
                                     'line_id2', 'From lines',
                                     copy=False)

    # def invoice_line_create(self, invoice_id, qty):
    #     """
    #     No crear lineas de factura si son promociones de descuento, que agrupan
    #     lineas del mismo precio unitario. Facturaremos las cantidades de las
    #     entregas de los albaranes parciales después.
    #     Las promociones que no tienen campo orig_line_ids, o si no son
    #     promociones, se facturan normalmente.
    #     """
    #     no_promo_ids = []
    #     lines_rec = self.env['sale.order.line']
    #     for l in self:
    #         if l.promotion_line and l.orig_line_ids:
    #             continue
    #         no_promo_ids.append(l.id)
    #         lines_rec.add(l)
    #     res = super(SaleOrderLine, lines_rec).invoice_line_create(invoice_id,
    #                                                               qty)
    #     return res
