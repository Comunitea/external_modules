# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _get_customer_prices_count(self):
        for tmpl in self:
            tmpl.customer_prices_count = len(tmpl.customer_tmpl_prices)

    customer_tmpl_prices = fields.One2many('customer.price', 'product_tmpl_id',
                                           'Customer Prices')
    customer_prices_count = fields.\
        Integer(compute='_get_customer_prices_count', string='#Prices')

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def _get_customer_prices_count(self):
        for prod in self:
            prod.customer_prices_count = len(prod.customer_product_prices)

    customer_product_prices = fields.One2many('customer.price', 'product_id',
                                              'Customer Prices')
    product_item_ids = fields.One2many('product.pricelist.item',
                                    'product_id',
                               'Pricelist Product Items')
    customer_prices_count = fields.\
        Integer(compute='_get_customer_prices_count', string='#Prices')
