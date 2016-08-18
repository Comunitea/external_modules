# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2013 QUIVAL, S.A. All Rights Reserved
#    $Pedro Gómez Campos$ <pegomez@elnogal.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, SUPERUSER_ID
from openerp.addons.decimal_precision import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    def get_price_from_cost_structure(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for move in self.browse(cr, uid, ids, context=context):
            if move.production_id and move.product_id.cost_structure_id:
                c = context.copy()
                c['cron'] = True
                c['product_id'] = move.product_id.id
                pcl_pool = self.pool.get('product.costs.line')
                cost = pcl_pool.get_product_costs(cr, uid, move.product_id, c)
                price = cost.get('inventory_cost', False)
                if price:
                    self.write(cr, uid, [move.id], {'price_unit': price},
                               context=context)

    def update_product_price(self, cr, uid, ids, context=None):
        """ Copy function of product_price_update_before_done with productions
            locations
        """
        product_obj = self.pool.get('product.product')
        tmpl_dict = {}
        for move in self.browse(cr, uid, ids, context=context):
            # Adapt standard price on incomming OR PRODUCTION moves if
            # the product cost_method is 'average'
            if (move.location_id.usage in ('supplier', 'production')) and \
                    (move.product_id.cost_method == 'average'):
                product = move.product_id
                prod_tmpl_id = move.product_id.product_tmpl_id.id
                qty_available = move.product_id.product_tmpl_id.qty_available
                # Becouse move is done and we dont want the move qty yet
                qty_available -= move.product_uom_qty
                if qty_available <= 0:
                    qty_available = 0.0
                if tmpl_dict.get(prod_tmpl_id):
                    product_avail = qty_available + tmpl_dict[prod_tmpl_id]
                else:
                    tmpl_dict[prod_tmpl_id] = 0
                    product_avail = qty_available
                if product_avail <= 0:
                    new_std_price = move.price_unit
                else:
                    # Get the standard price
                    amount_unit = product.standard_price
                    new_std_price = ((amount_unit * product_avail) +
                                     (move.price_unit * move.product_qty)) /\
                        (product_avail + move.product_qty)
                tmpl_dict[prod_tmpl_id] += move.product_qty
                # Write the standard price, as SUPERUSER_ID because  warehouse
                # manager may not have the right to rite on products
                ctx = dict(context or {}, force_company=move.company_id.id)
                product_obj.write(cr, SUPERUSER_ID, [product.id],
                                  {'standard_price': new_std_price},
                                  context=ctx)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    cost = fields.Float('Unit Cost', digits=dp.get_precision('Product Price'))


# class StockHistory(models.Model):
#     """
#     Added to reload stock_history view, because is deleted when we put the
#     precission to the stock quant cost field
#     """
#     _inherit = 'stock.history'

#     def init(self, cr):
#         super(StockHistory, self).init(cr)
