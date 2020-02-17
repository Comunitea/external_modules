# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2019 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
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

from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)

class InfoApk(models.Model):
    _name = 'info.apk'

    def return_tree_fields(self):
        return ['id', 'display_name']

    @api.model
    def get_apk_object(self, values):
        domain = values.get('domain', [])
        fields = values.get('fields', ['id', 'display_name'])
        model = values.get('model', False)
        if not model: return []
        obj_ids = self.env[model].search(domain)
        vals = []

        for obj in obj_ids:
            val_obj = {}
            for field in fields:
                f_obj = obj.fields_get()[field]
                if f_obj['type'] in ['many2many', 'one2many']:
                    domain = [('id', 'in', obj[field].ids)]
                    fields = self.return_tree_fields()
                    model = f_obj['relation']
                    values = {'domain': domain, 'fields': fields, 'model': model}
                    val_obj[field] = self.env[model].get_apk_object(values)
                elif f_obj['type'] == 'many2one':
                    f_tree_vals = []
                    for f_tree in self.env[f_obj['relation']].return_tree_fields():
                        f_tree_vals.append(obj[field][f_tree])
                    val_obj[field] = f_tree_vals
                else:
                    val_obj[field] = obj[field]

            vals.append(val_obj)
        print (vals)
        return  vals



class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'info.apk']

class StockMoveLine(models.Model):
    _name = 'stock.move.line'
    _inherit = ['stock.move.line', 'info.apk']

class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'info.apk']


class StockLocation(models.Model):
    _name = 'stock.location'
    _inherit = ['stock.location', 'info.apk']