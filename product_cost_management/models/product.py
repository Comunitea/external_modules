# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos All Rights Reserved
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
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
import time
from openerp.tools.translate import _


def rounding(f, r):
    if not r:
        return f
    return round(f / r) * r


class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
        'cost_structure_id': fields.property(type='many2one',
                                             relation='cost.structure',
                                             string="Cost Structure")
    }

    def action_show_product_costs(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        prod_cost_line_obj = self.pool.get('product.costs.line')
        value = prod_cost_line_obj.show_product_costs(cr, uid, ids, context)

        return value

    def action_get_product_costs(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        prod_cost_line_obj = self.pool.get('product.costs.line')
        value = prod_cost_line_obj.get_product_costs(cr, uid, ids, context)

        return value

    def action_update_product_costs(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        prod_cost = self.pool.get('product.cost')
        line = self.pool.get('product.cost.lines')
        prod = self.pool.get('product.product')
        vals = {}

        if context.get('product_id', False):
            pro = [context['product_id']]
        else:
            pro = prod.search(cr, uid, [])
        for product in prod.browse(cr, uid, pro):
            if product.cost_structure_id and product.cost_structure_id.elements:
                cost_ids = prod_cost.search(cr,
                                            uid,
                                            [('product_id', '=', product.id)],
                                            order="date desc")
                if cost_ids:
                    lines = line.search(cr,
                                        uid,
                                        [('product_cost_id', '=', cost_ids[0]),
                                         ('total', '=', True),
                                         ('inventory', '=', True)],
                                        order="sequence desc")
                    if lines:
                        line_cost = line.browse(cr, uid, lines[0])
                        vals = {'theoric_cost':
                                line_cost.theoric_cost}
        return vals


class product_cost(osv.osv):
    _name = 'product.cost'
    _rec_name = "product_id"

    _columns = {
        'product_id': fields.many2one('product.product', 'Product Cost',
                                      required=True),
        'product_cost_lines': fields.one2many('product.cost.lines',
                                              'product_cost_id', 'Costs'),
        'date': fields.datetime('Date', required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True),
    }
    _defaults = {
        'company_id': lambda s, cr, uid, c:
        s.pool.get('res.company')._company_default_get(cr, uid,
                                                       'product.cost',
                                                       context=c),
    }


class product_cost_lines(osv.osv):
    _name = 'product.cost.lines'

    def _cost_percent(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for prod_cost_line in self.browse(cr, uid, ids, context):
            res[prod_cost_line.id] = {
                'tc_rc_percent': 0.0,
            }

            if prod_cost_line.real_cost:
                res[prod_cost_line.id]['tc_rc_percent'] = 100 * ((prod_cost_line.theoric_cost / prod_cost_line.real_cost) - 1)
            else:
                res[prod_cost_line.id]['tc_rc_percent'] = 100

        return res

    _columns = {
        'product_cost_id': fields.many2one('product.cost', 'Cost', required=True, ondelete='cascade'),
        'sequence': fields.integer('Sequence', required=True),
        'name': fields.char('Name', size=255, required=True),
        'theoric_cost': fields.float('Theoric Cost', required=True, digits=(16,3)),
        'real_cost': fields.float('Real Cost', required=True, digits=(16, 3)),
        'tc_rc_percent': fields.function(_cost_percent, method=True,
                                         string=_('TC vs RC (%)'), type='float',
                                         digits=(4, 2), multi='cost_percent'),
        'inventory': fields.boolean('Inventory'),
        'total': fields.boolean('Total'),
        'company_id': fields.related('product_cost_id', 'company_id',
                                     type='many2one', relation='res.company',
                                     string='Company', store=True, readonly=True),
    }
    _defaults = {
        'theoric_cost': 0.0,
        'real_cost': 0.0,
        'inventory': False,
        'total': False,
    }
