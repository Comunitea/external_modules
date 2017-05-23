# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _
from openerp.exceptions import except_orm


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def get_product_info(self, product_id, partner_id):
        """ Return data of widget productInfo """

        res = {
            'stock': 0.0,
            'last_date': "-",
            'last_qty': 0.0,
            'last_price': 0.0,
        }
        t_sol = self.env['sale.order.line']
        if not product_id or not partner_id:
            raise except_orm(_('Error!'), _("Product_id or partrner_id \
                                            must be defined"))
        product_obj = self.browse(product_id)
        res['stock'] = product_obj.virtual_available
        domain = [('product_id', '=', product_id),
                  ('order_id.partner_id', '=', partner_id),
                  ('state', 'in', ['sale', 'done']),
                  ]
        line_obj = t_sol.search(domain, limit=1, order="id desc")
        if line_obj:  # Last sale info
            res['last_date'] = line_obj.order_id.date_order
            res['last_qty'] = line_obj.product_uom_qty
            res['last_price'] = line_obj.price_unit
        return res

    @api.model
    def _get_line_discount(self, line):
        return line.discount

    @api.model
    def get_history_product_info(self, product_id, partner_id):
        """ Return data of widget productInfo History """
        res = []
        t_sol = self.env['sale.order.line']
        if not product_id or not partner_id:
            raise except_orm(_('Error!'), _("Product_id or partrner_id \
                                            must be defined"))
        domain = [('product_id', '=', product_id),
                  ('order_id.partner_id', '=', partner_id),
                  ('state', 'in', ['sale', 'done']),
                  ]
        lines_objs = t_sol.search(domain, order="id desc")
        for line in lines_objs:
            vals = {
                'date': line.order_id.date_order,
                'qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'discount': self._get_line_discount(line)
            }
            res.append(vals)
        return res

    @api.model
    def _get_product_values2(self, product, partner_id, pricelist_id):
        onchange_vals = self._get_onchange_vals(product, partner_id,
                                                pricelist_id)

        vals = {
            'id': product.id,
            'display_name': product.display_name,
            'default_code': product.default_code,
            'stock': self._get_product_stock(product),
            'price': onchange_vals['price'],
            'discount': 0.0,
            'qty': 0.0,
            'tax_ids': onchange_vals['tax_ids'],
        }
        return vals

    @api.model
    def ts_search_products(self, product_name, partner_id, pricelist_id):
        limit = 100000
        res = []
        domain = [('name', 'ilike', product_name)]
        if not product_name:
            limit = 100
        for product in self.search(domain, limit=limit):
            values = self._get_product_values2(product, partner_id,
                                               pricelist_id)
            res.append(values)
        return res

    @api.model
    def _get_onchange_vals(self, product, partner_id, pricelist_id):
        res = {
            'price': 0.0,
            'tax_ids': []
        }
        if partner_id and product:
            values = self.env['sale.order.line'].\
                ts_product_id_change(product.id, partner_id, pricelist_id)
            res.update({
                'price': values.get('price_unit', 0.0),
                'tax_ids': values.get('tax_id', [])
            })
        return res

    @api.model
    def _get_product_stock(self, product):
        return product and product.qty_available or 0
