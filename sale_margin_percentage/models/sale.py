# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos (<http://www.comunitea.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.one
    @api.depends("product_uom_qty", "price_unit", "discount", "product_id")
    def _product_margin(self):
        self.margin = 0.0
        self.margin_perc = 0.0
        self.purchase_price = 0.0
        c = self._context.copy()
        c.update(company_id=self.order_id.company_id.id)
        t_product = self.env['product.product'].with_context(c)
        product = False
        if self.product_id:
            product = t_product.browse(self.product_id.id)
        if product and product.standard_price:
            self.purchase_price = product.standard_price
            sale_price = self.price_unit * self.product_uom_qty * \
                ((100.0 - self.discount) / 100.0)
            purchase_price = self.purchase_price * self.product_uom_qty
            margin = round(sale_price - purchase_price, 2)
            if sale_price:
                self.margin_perc = round((margin * 100) / sale_price, 2)
            self.margin = margin

    margin = fields.Float(compute="_product_margin", string='Margin',
                          store=True, multi='marg', readonly=True)
    margin_perc = fields.Float(compute="_product_margin", string='Margin %',
                               store=True, multi='marg', readonly=True)
    purchase_price = fields.Float(compute="_product_margin", readonly=True,
                                  string="Purchase price", store=True,
                                  multi='marg')


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.one
    @api.depends("order_line.margin")
    def _product_margin(self):
        total_purchase = self.total_purchase

        self.margin = 0.0
        sale_price = margin = 0.0
        if total_purchase != 0:
            for line in self.order_line:
                margin += line.margin or 0.0
                sale_price += line.price_subtotal
            self.margin = round(margin, 2)
            if sale_price:
                self.margin_perc = round((margin * 100) / sale_price, 2)

    @api.one
    def _get_total_price_purchase(self):
        self.total_purchase = 0.0
        for line in self.order_line:
            if line.purchase_price:
                self.total_purchase += line.purchase_price * \
                    line.product_uom_qty
            elif line.product_id:
                c = self._context.copy()
                c.update(company_id=self.order_id.company_id.id)
                t_product = self.env['product.product'].with_context(c)
                product = t_product.browse(self.product_id.id)
                cost_price = product.standard_price
                self.total_purchase += cost_price * \
                    line.product_uom_qty

    total_purchase = fields.Float(compute="_get_total_price_purchase",
                                  string='Price purchase', readonly=False)
    margin = fields.Float(compute="_product_margin", string='Margin',
                          help="It gives profitability by calculating "
                               "percentage.", store=True, readonly=True)
    margin_perc = fields.Float(compute="_product_margin", string='Margin %',
                               store=True, readonly=True)
