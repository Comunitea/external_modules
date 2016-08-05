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

COST_TYPES = [('total', 'Total'),
              ('bom', 'BoM'),
              ('standard_price', 'Cost price'),
              ('ratio', 'Ratio'),
              ('inventory', 'Inventory')]
DISTRIBUTION_MODES = [('eur', 'By amounting'),
                      ('units', 'By units'),
                      ('kg', 'By weight net (kg)'),
                      ('min', 'By minutes')]
MODELS = [('sales.forecast', 'Sales forecast'),
          ('forecast.kg.sold', 'Kg sold forecast'),
          ('mrp.forecast', 'Hour forecast')]


class cost_type(osv.osv):
    _name = 'cost.type'
    _description = ''
    _columns = {
        'name': fields.char('Cost name', size=255, required=True),
        'cost_type': fields.selection(COST_TYPES, 'Cost type', required=True,
            help="This option is used to define how the cost is calculated.\n" \
            "The 'Total' value means that the cost is a totalizing of the preceding lines in the structure sequence.\n"\
            "The 'BoM' value means that the cost is calculated from the product BoM.\n"\
            "The 'Cost price' value means that the cost is the cost price that currently has the product.\n"\
            "The 'Ratio' value means that the cost is calculated based on a ratio.\n"\
            "The 'Inventory' value means that the cost is as total and when update product cost it will be used as the 'Cost price'."
            ),
        'cost_ratio': fields.float('Cost ratio'),
        'distribution_mode': fields.selection(DISTRIBUTION_MODES, 'Distribution mode'),
        'budget_item': fields.many2one('budget.item', 'Budget Item'),
        'forecast_type': fields.reference('Forecast', MODELS, size=128),
        'forecast_cost_ratio': fields.float('Forecasted cost ratio', readonly=True), # TODO: campo funcion
        'real_cost_ratio': fields.float('Real cost ratio', readonly=True), # TODO: campo funcion
        'company_id': fields.many2one('res.company', 'Company', required=True),
    }
    _defaults = {
        'cost_type': 'total',
        'company_id': lambda s, cr, uid, c:
        s.pool.get('res.company')._company_default_get(cr, uid, 'cost.type',
                                                       context=c),
    }

