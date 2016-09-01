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
from openerp import models, _
from openerp.osv import fields


COST_TYPES = [('total', 'Total'),
              ('bom', 'BoM'),
              ('standard_price', 'Cost price'),
              ('ratio', 'Ratio'),
              ('inventory', 'Inventory')]
DISTRIBUTION_MODES = [('eur', 'By amounting'),
                      ('units', 'By units'),
                      ('kg', 'By weight net (kg)'),
                      ('min', 'By minutes')]
FIELD_THEORIC_COST = [('fixed_price', 'Fixed Price'),
                      ('theoric_cost', 'Theoric cost')]
TIME = [('current_year', 'Current Year')]


COST_THEORIC_TYPES = [('none', 'None'),
                      ('ldm', 'LdM'),
                      ('budget_item', 'Budget item')]
COST_REAL_TYPES = [('none', 'None'),
                   ('ldm', 'LdM'),
                   ('analytic_account', 'Analytic Account'),
                   ('based_productions', 'Based on Production Orders')]
FIELD_REAL_COST = [('fixed_price', 'Fixed Price'),
                   ('pmp', 'PMP')]
DISTRIBUTE_BUDGET_ITEM = [('kg', 'By weight (net)(kg)'),
                          ('eur', 'By sales volume')]


class cost_structure(models.Model):
    _name = 'cost.structure'
    _description = ''
    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'elements': fields.one2many('cost.structure.elements', 'structure_id',
                                    'Elements', required=True),
        'year': fields.integer('Year', size=4, required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True),
    }
    _defaults = {
        'name': '/',
        'company_id': lambda s, cr, uid, c:
        s.pool.get('res.company')._company_default_get(cr, uid,
                                                       'cost.structure',
                                                       context=c),
    }

    def _check_elements_required(self, cr, uid, ids, context=None):
        for cost_str in self.browse(cr, uid, ids, context):
            total_type = inventory_type = False
            for e in cost_str.elements:
                if e.cost_type == 'total':
                    total_type = True
                if e.cost_type == 'inventory':
                    inventory_type = True
            return (total_type and inventory_type)

    _constraints = [(_check_elements_required,
                     _('You must define a element with total cost type and\
                       another of inventory cost type'),
                     ['elements'])]


class cost_structure_elements(models.Model):
    _name = 'cost.structure.elements'
    _description = ''
    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'sequence': fields.integer('Sequence', required=True),
        'structure_id': fields.many2one('cost.structure', 'Structure',
                                        required=True, ondelete='cascade'),
        'cost_type_id': fields.many2one('cost.type', 'Cost name', required=True),
        'cost_type': fields.related('cost_type_id', 'cost_type', type="selection",
                                    selection=COST_TYPES, relation="cost.type",
                                    string="Cost type", readonly=True,
                                    store=False,
            help="This option is used to define how the cost is calculated.\n" \
            "The 'Total' value means that the cost is a totalizing of the preceding lines in the structure sequence.\n"\
            "The 'BoM' value means that the cost is calculated from the product BoM.\n"\
            "The 'Cost price' value means that the cost is the cost price that currently has the product.\n"\
            "The 'Ratio' value means that the cost is calculated based on a ratio.\n"\
            "The 'Inventory' value means that the cost is as total and when update product cost it will be used as the 'Cost price'."
            ),
        'cost_ratio': fields.related('cost_type_id', 'cost_ratio', type="float",
                                     relation="cost.type", string="Cost ratio",
                                     readonly=True, store=False),
        'distribution_mode': fields.related('cost_type_id', 'distribution_mode',
                                            type="selection", selection=DISTRIBUTION_MODES,
                                            relation="cost.type", string="Distribution mode",
                                            readonly=True, store=False),
        'time': fields.selection(TIME, string="Time"),
        'company_id': fields.related('structure_id', 'company_id', type='many2one',
                                     relation='res.company', string='Company',
                                     store=True, readonly=True),
        #'total': fields.boolean('Total')
    }
    _defaults = {
        'name': '/',
        'sequence': 10,
    }
    _order = 'sequence asc, id asc'
