# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
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

class sale_order_line(orm.Model):

    _inherit = 'sale.order.line'
    _columns = {
        'warehouse_id': fields.many2one('stock.warehouse', 'Source warehouse', readonly=True, states={'draft': [('readonly', False)]}),
        'method': fields.selection(
                    [('direct_delivery', 'Direct delivery')],
                    string='Method',
                    readonly=True,
                    states={'draft': [('readonly', False)]}),
    }
    _defaults = {
        'method': 'direct_delivery'
    }


class sale_order(orm.Model):

    _inherit = 'sale.order'

    def _prepare_order_line_procurement(self, cr, uid, order, line, group_id=False, context=None):
        res = super(sale_order,self)._prepare_order_line_procurement(cr, uid, order, line, group_id, context=context)
        if line.warehouse_id and line.method == 'direct_delivery':
            res['warehouse_id'] = line.warehouse_id.id
        return res

