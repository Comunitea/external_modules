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
        offset = values.get('offset', 0)
        limit = values.get('limit', 0)
        model = values.get('model', False)
        if not model: return []
        fields = values.get('fields', self.env[model].return_tree_fields())
        obj_ids = self.env[model].search(domain, offset=offset, limit=limit)
        vals = []

        for obj in obj_ids:
            val_obj = {}
            fields_to_remove = self.get_fields_to_remove(model, obj)
            allowed_fields = [x for x in fields if x not in fields_to_remove]
            for field in allowed_fields:
                f_obj = obj.fields_get()[field]
                if f_obj['type'] in ['many2many', 'one2many']:
                    domain = [('id', 'in', obj[field].ids)]
                    sub_model = f_obj['relation']
                    values = {'domain': domain, 'model': sub_model}
                    val_obj[field] = self.env['info.apk'].get_apk_object(values)
                elif f_obj['type'] == 'many2one':
                    f_tree_vals = []
                    for f_tree in self.env[f_obj['relation']].return_tree_fields():
                        if obj[field].fields_get()[f_tree]['type'] in ['many2many', 'one2many', 'many2one']:
                            f_tree_domain = [('id', 'in', obj[field][f_tree].ids)]
                            f_tree_model = obj[field].fields_get()[f_tree]['relation']
                            values = {'domain': f_tree_domain, 'model': f_tree_model}
                            f_tree_vals.append( self.env['info.apk'].get_apk_object(values))
                        elif obj[field].fields_get()[f_tree]['type'] == 'many2one':
                            t_tree_vals = []
                            for t_tree in self.env[obj[field].fields_get()[f_tree]['relation']].return_tree_fields():
                                t_tree_vals.append(obj[field][f_tree][t_tree])
                            f_tree_vals.append(t_tree_vals)
                        else:
                            f_tree_vals.append(obj[field][f_tree])
                    val_obj[field] = f_tree_vals
                else:
                    val_obj[field] = obj[field]
            vals.append(val_obj)
        return  vals

    def get_fields_to_remove(self, model, obj):
        if model == 'stock.picking':
            return obj.picking_fields.split(",")
        elif model == 'stock.move.line':
            return obj.picking_id.move_line_fields.split(",")
        elif model == 'stock.move':
            return obj.picking_id.move_fields.split(",")
        else:
            return []


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'display_name', 'default_code', 'list_price', 'qty_available', 'virtual_available']

class StockMoveLine(models.Model):
    _name = 'stock.move.line'
    _inherit = ['stock.move.line', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'product_id', 'product_uom_qty', 'qty_available', 'qty_done', 'location_id', 'location_dest_id', 'lot_id',
                'package_id', 'result_package_id', 'tracking']

class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ['stock.move', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'product_id', 'product_uom_qty', 'reserved_availability', 'quantity_done', 'tracking']

class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'display_name', 'location_id', 'location_dest_id', 'scheduled_date', 'state', 'picking_fields', 'move_fields', 'move_line_fields']

class StockLocation(models.Model):
    _name = 'stock.location'
    _inherit = ['stock.location', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'display_name', 'usage', 'company_id']

class StockQuant(models.Model):
    _name = 'stock.quant'
    _inherit = ['stock.quant', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'product_id', 'reserved_quantity', 'quantity', 'location_id']

class StockQuantPackage(models.Model):
    _name = 'stock.quant.package'
    _inherit = ['stock.quant.package', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'display_name', 'packaging_id']

class StockProductionLot(models.Model):
    _name = 'stock.production.lot'
    _inherit = ['stock.production.lot', 'info.apk']

    def return_tree_fields(self):
        return ['display_name', 'ref']

class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = ['res.company', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'display_name']

class ProductUom(models.Model):
    _name = 'product.uom'
    _inherit = ['product.uom', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'display_name']

class StockPickingType(models.Model):
    _name = 'stock.picking.type'
    _inherit = ['stock.picking.type', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'name', 'color', 'warehouse_id', 'code']

class PickingTypeGroupCode(models.Model):
    _name = 'picking.type.group.code'
    _inherit = ['picking.type.group.code', 'info.apk']

    def return_tree_fields(self):
        return ['code', 'display_name', 'app_integrated', 'picking_fields', 'move_fields', 'move_line_fields']

class StockWarehouse(models.Model):
    _name = 'stock.warehouse'
    _inherit = ['stock.warehouse', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'display_name']

class ProductCategory(models.Model):
    _name = 'product.category'
    _inherit = ['product.category', 'info.apk']

    def return_tree_fields(self):
        return ['id', 'display_name']