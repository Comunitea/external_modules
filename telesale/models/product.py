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
    def _get_product_values(self, product):
        vals = {
            'id': product.id,
            'display_name': product.display_name,
            'default_code': product.default_code,
            'stock': product.qty_available
        }
        return vals

    @api.model
    def ts_search_products(self, product_name):
        res = []
        domain = [('name', 'ilike', product_name)]
        for product in self.search(domain):
            values = self._get_product_values(product)
            res.append(values)
        return res
