# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def ts_product_id_change(self, product_id, partner_id):
        res = {}

        order_t = self.env['sale.order']
        partner = self.env['res.partner'].browse(partner_id)
        with self.env.do_in_draft():
            order = order_t.create({'partner_id': partner_id,
                                    'pricelist_id':
                                    partner.property_product_pricelist.id})
            line = self.create({'order_id': order.id,
                                'product_id': product_id})
        line.product_id_change()
        res.update({
            'price_unit': line.price_unit,
            'product_uom': line.product_uom.id,
            'product_uom_qty': line.product_uom_qty,
            'tax_id': [x.id for x in line.tax_id]

        })
        return res
