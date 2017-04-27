# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, fields


# class ProductProduct(models.Model):
#     _inherit = 'product.product'

#     route_name = fields.Char('Route name', related='route_ids.name',
#                              store=True)

#     # Ejemplo de como añadir mas campos al widget
#     # @api.model
#     # def get_product_info(self, product_id, partner_id):
#     #     """ Return data of widget productInfo """
#     #     res = super(ProductProduct, self).get_product_info(product_id,
#     #                                                        partner_id)
#     #     product_obj = self.browse(product_id)
#     #     route = product_obj.route_ids[0].name if product_obj.route_ids else ""
#     #     lqdr = _("Yes") if product_obj.lqdr else _("No")
#     #     res.update({'route': route, 'lqdr': lqdr})
#     #     return res


#     @api.model
#     def ts_get_global_stocks(self, product_id):
#         """ Return data of widget productInfo """
#         res = {'global_available_stock': 0.0}
#         if product_id:
#             product_obj = self.browse(product_id)
#             res.update({'global_available_stock':
#                         product_obj.global_available_stock})
#         return res
