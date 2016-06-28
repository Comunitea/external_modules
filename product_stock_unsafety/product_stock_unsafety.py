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
from openerp.osv import orm, fields
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
STATES = [('in_progress', 'In Progress'),
          ('finalized', 'Finalized'),
          ('exception', 'Exception'),
          ('cancelled', 'Cancelled')]


class product_stock_unsafety(orm.Model):
    _name = 'product.stock.unsafety'
    _description = 'Products that have stock under minimum'
    _columns = {
        'product_id': fields.many2one('product.product',
                                      'Product',
                                      required=True),
        'supplier_id': fields.many2one('res.partner',
                                       'Supplier'),
        'min_fixed': fields.float('Min. Fixed', readonly=True),
        'max_fixed': fields.float('Max. Fixed', readonly=True),
        'real_stock': fields.float('Real Stock', readonly=True),
        'virtual_stock': fields.float('Virtual Stock', readonly=True),
        'purchase_id': fields.many2one('purchase.order.line',
                                       'Purchase'),
        'product_qty': fields.float('Qty ordered'),
        'date_delivery': fields.date('Delivery'),
        'responsible': fields.many2one('res.users',
                                       'Responsible'),
        'state': fields.selection(STATES, 'State', readonly=True),
        'date': fields.date('Date'),
        'name': fields.char('Reason', size=64),
        'incoming_qty': fields.related('product_id',
                                       'incoming_qty',
                                       type='float',
                                       string='Incoming qty.'),
        'minimum_proposal': fields.float('Min. Proposal'),
        'company_id': fields.many2one('res.company', 'Company')
    }
    _defaults = {
        'date':  fields.date.context_today
    }

    def cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'cancelled'})
        return True

    def write_purchase_id(self, cr, uid, ids, purchase_line_id=False,
                          product_id=False, context=None):
        """
        Function you are looking if exists under minimum for he product
        received in progress state and has not linked purchase order line.
        If found, writes it the purchase order line that just created.
        """
        if context is None:
            context = {}
        mins = []
        undermin = self.pool.get('product.stock.unsafety')
        purl = self.pool.get('purchase.order.line')
        if product_id and purchase_line_id:
            # Find under minimums that satisfying the conditions
            # indicated.
            mins = undermin.search(cr, uid, [('product_id', '=', product_id),
                                             ('state', '=', 'in_progress'),
                                             ('purchase_id', '=', False)])
            if mins:
                # Writes the first under minimum found the purchase
                # order line that was just created
                purline = purl.browse(cr, uid, purchase_line_id)
                undermin.write(cr,
                               uid,
                               mins[0],
                               {'purchase_id': purchase_line_id,
                                'product_qty': purline.product_qty})
        return {}

    def create_or_write(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        ids = self.search(cr, uid, [('state', '=', vals['state']),
                                    ('product_id', '=', vals['product_id']),
                                    ('supplier_id', '=', vals['supplier_id'])],
                          context=context)
        if vals['state'] == 'in_progress':
            ids += self.search(cr, uid, [('state', '=', 'exception'),
                                    ('product_id', '=', vals['product_id']),
                                    ('supplier_id', '=', False)], context=context)
        if ids:
            self.write(cr, uid, ids, vals, context=context)
        else:
            self.create(cr, uid, vals, context=context)
