# © 2014 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.depends('order_line.margin')
    @api.multi
    def _product_margin_perc(self):
        for sale in self:
            margin = 0.0
            if sale.amount_untaxed:
                for line in sale.order_line:
                    margin += line.margin or 0.0
                sale.margin_perc = round((margin * 100) /
                                         sale.amount_untaxed, 2)

    @api.depends('order_line.margin')
    @api.multi
    def _get_total_price_purchase(self):
        for sale in self:
            total_purchase = 0.0
            for line in sale.order_line:
                if line.product_id:
                    if line.purchase_price:
                        total_purchase += line.purchase_price * \
                            line.product_uom_qty
                    else:
                        total_purchase += line.product_id.standard_price * \
                            line.product_uom_qty
            sale.total_purchase = total_purchase

    total_purchase = fields.Float(compute="_get_total_price_purchase",
                                  string='Price purchase', store=True)
    margin_perc = fields.Float(compute="_product_margin_perc",
                               string='Margin %',
                               help="It gives profitability by calculating "
                                    "percentage.", store=True)


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.one
    @api.depends('margin')
    def _product_margin_perc(self):
        if self.purchase_price:
            cost_price = self.purchase_price
        else:
            cost_price = self.product_id.standard_price
        if cost_price:
            self.margin_perc = round((self.margin * 100) /
                                     (cost_price * self.product_uom_qty), 2)

    margin_perc = fields.Float('Margin', compute='_product_margin_perc',
                               store=True)
