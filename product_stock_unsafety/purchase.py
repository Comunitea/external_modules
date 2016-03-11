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


class purchase_order_line(orm.Model):
    _inherit = 'purchase.order.line'

    def create(self, cr, uid, vals, context=None):
        """
        When a purchase order line is created, calls the function that
        link the same object with under minimal.
        """
        if context is None:
            context = {}
        undermin = self.pool.get('product.stock.unsafety')
        res = super(purchase_order_line, self).create(cr,
                                                      uid,
                                                      vals,
                                                      context=context)
        undermin.write_purchase_id(cr,
                                   uid,
                                   [],
                                   res,
                                   vals['product_id'],
                                   context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        """
        Function that monitors when a product is written on a purchase
        order line, then calls the function that links the purchase order
        lines to under minimums.
        In addition, it also monitors when the line status of the
        purchase order changes to 'done', then if it is linked to under
        minimums with 'in progress' status, it ends.
        """
        if context is None:
            context = {}
        undermin = self.pool.get('product.stock.unsafety')
        res = super(purchase_order_line, self).write(cr,
                                                     uid,
                                                     ids,
                                                     vals,
                                                     context=context)
        for cur in self.browse(cr, uid, ids):
            if vals.get('product_id', False):
                undermin.write_purchase_id(cr,
                                           uid,
                                           [],
                                           cur.id,
                                           vals['product_id'],
                                           context=context)
            if vals.get('state', False) and vals['state'] == 'confirmed':
                mins = undermin.search(cr,
                                       uid,
                                       [('purchase_id', '=', cur.id),
                                        ('state', '=', 'in_progress')])
                if mins:
                    undermin.write(cr, uid, mins[0], {'state': 'finalized'})
        return res


class purchase_order(orm.Model):
    _inherit = 'purchase.order'

    def write(self, cr, uid, ids, vals, context=None):
        """
        Monitors when the line status of the
        purchase order changes to 'done', then if it is linked to under
        minimums with 'in progress' status, it ends.
        """
        if context is None:
            context = {}
        undermin = self.pool.get('product.stock.unsafety')
        for cur in self.browse(cr, uid, ids):
            if vals.get('state', False) and vals['state'] == 'confirmed':
                if cur.order_line:
                    for l in cur.order_line:
                        domain = [('purchase_id', '=', l.id),
                                  ('state', '=', 'in_progress')]
                        mins = undermin.search(cr, uid, domain)
                        if mins:
                            undermin.write(cr,
                                           uid,
                                           mins[0],
                                           {'state': 'finalized'})
        res = super(purchase_order, self).write(cr,
                                                uid,
                                                ids,
                                                vals,
                                                context=context)
        return res
