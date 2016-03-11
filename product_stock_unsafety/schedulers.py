# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2014 Pexego Sistemas Informáticos All Rights Reserved
#    $Marta Vázquez Rodríguez$ <marta@pexego.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
from openerp.osv import orm
from openerp import pooler
from openerp.tools.translate import _
from datetime import date
from psycopg2 import OperationalError
import openerp


class procurement_order(orm.Model):
    _inherit = 'procurement.order'

    def _procure_orderpoint_confirm(self, cr, uid, use_new_cursor=False, company_id = False, context=None):
        '''
        Create procurement based on Orderpoint

        :param bool use_new_cursor: if set, use a dedicated cursor and auto-commit after processing each procurement.
            This is appropriate for batch jobs only.
        '''
        if context is None:
            context = {}
        if use_new_cursor:
            cr = openerp.registry(cr.dbname).cursor()
        orderpoint_obj = self.pool.get('stock.warehouse.orderpoint')
        stock_unsafety = self.pool.get('product.stock.unsafety')
        procurement_obj = self.pool.get('procurement.order')
        prod_obj = self.pool.get('product.product')
        prod_ids = prod_obj.search(cr, uid, [])
        for prod in prod_obj.browse(cr, uid, prod_ids):
            orderpoint_ids = orderpoint_obj.search(cr, uid, [('product_id', '=', prod.id),
                                                             ('from_date', '<=', date.today()),
                                                             ('to_date', '>=', date.today()), ], offset=0, limit=None)
            if not orderpoint_ids:
                orderpoint_ids = orderpoint_obj.search(cr, uid, [('product_id', '=', prod.id),
                                                                 ('from_date', '=', False),
                                                                 ('to_date', '=', False)], offset=0, limit=None)
            if not orderpoint_ids:
                orderpoint_ids = []

            for op in orderpoint_obj.browse(cr, uid, orderpoint_ids, context=context):
                try:
                    seller = False
                    prods = self._product_virtual_get(cr, uid, op)
                    if prods is None:
                        continue
                    if prods < op.product_min_qty:
                        if prod.seller_ids:
                            seller = prod.seller_ids[0].name.id
                            state = 'in_progress'
                        else:
                            state = 'exception'
                        vals = {'product_id': prod.id,
                                'supplier_id': seller,
                                'min_fixed': op.product_min_qty,
                                'max_fixed': op.product_max_qty,
                                'real_stock': prod.qty_available,
                                'virtual_stock': prods,
                                'responsible': uid,
                                'state': state,
                                'name': 'stock minimo',
                                'company_id': op.company_id.id}
                        stock_unsafety.create_or_write(cr, uid, vals,
                                                       context=context)
                        if use_new_cursor:
                            cr.commit()
                except OperationalError:
                    if use_new_cursor:
                        orderpoint_ids.append(op.id)
                        cr.rollback()
                        continue
                    else:
                        raise
            if use_new_cursor:
                cr.commit()

        if use_new_cursor:
            cr.commit()
            cr.close()
        return {}
