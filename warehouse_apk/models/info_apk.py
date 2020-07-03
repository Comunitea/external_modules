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
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import logging
import pprint


_logger = logging.getLogger(__name__)

class InfoApk(models.AbstractModel):
    _name = 'info.apk'

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.display_name

    apk_name = fields.Char(compute="compute_apk_name")
    apk_warehouse_id = fields.Many2one('stock.warehouse', compute="compute_warehouse_id")


    def get_apk_product(self, code):
        product_domain = [('wh_code', '=', code)]
        product_id = self.env['product.product'].search(product_domain)
        if len(product_id)>1:
            raise ValueError ('Se han encontrado varios productos para este código {}'.format(code))
        return product_id

    def get_apk_lot(self, code, product_id):
        if code == product_id.wh_code or code == product_id.default_code:
            return False
        domain = [('name', '=', code)]
        if product_id:
            domain += [('product_id', '=', product_id.id)]
        lot_id = self.env['stock.production.lot'].search(domain)
        if len(lot_id)>1:
            raise ValueError ('Se han encontrado varios lotes para este código {}'.format(code))
        return lot_id

    def get_apk_location(self, code):
        domain = [('barcode', '=', code)]
        location_id = self.env['stock.location'].search(domain)
        if len(location_id) > 1:
            raise ValueError('Se han encontrado varias ubicaciones para este código {}'.format(code))
        return location_id

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.display_name

    @api.multi
    def compute_warehouse_id(self):

        company_user = self.env.user.company_id
        wh_id = self.env['stock.warehouse'].search([('company_id', '=', company_user.id)], limit=1)
        for loc in self:
            loc.apk_warehouse_id = wh_id.id

    def return_fields(self, mode='tree'):
        return ['id', 'display_name']

    def selection_dict(self, f_obj, field_value):
        selection = [x for x in f_obj['selection'] if x[0] == field_value]
        if not selection:
            return {'name': 'Indefinido', 'value': False}
        val = {'name': [x for x in f_obj['selection'] if x[0] == field_value][0][1],
               'value': field_value}
        return val

    def get_many2one_dict_values(self, field):
        many2one = self.fields_get()[field]
        options = self.env[many2one['relation']].read_group([('wh_code', '!=', False)], ['id'], ['wh_code'])
        res = []
        for option in options:
            res.append({'name': option['wh_code'], 'value' : option['wh_code']})
        return res

    def get_selection_dict_values(self, field):
        selection = self.fields_get()[field]['selection']
        res = []
        for option in selection:
            res.append({'name': option[1], 'value': option[0]})
        return res

    def m2o_dict(self, field):
        if field:
            return {'id': field.id, 'name': field.apk_name}
        else:
            return {'id': False}

    def m2m_dict(self, m2m_ids):
        val = []
        list_ids = []
        for m2m in m2m_ids:
            val.append({'id': m2m.id, 'name': m2m.apk_name})
            list_ids += [m2m.id]
        return val, list_ids


    def find_model_object(self, domain=[], search_str='', ids = []):
        if ids:
            domain += [('id', 'in', ids)]
        domain += [('name', '=', search_str)]
        res = self.search_read(domain, ['id', 'apk_name'])
        return [{'id': x['id'], 'name': x['apk_name']} for x in res]

    @api.model
    def find_apk_object(self, values):
        #print ("Valores de busqueda: \n{}".format(values))
        # devuelvo modelo e id
        model = values.get('model', False)
        ids = values.get('ids', [])
        domain = values.get('domain', [])
        search_str = values.get('search_str', '')
        return self.env[model].find_model_object(domain, search_str, ids)

    @api.model
    def get_modal_info(self, values):
        id = int(values.get('id'))
        obj = self.browse(id)
        fields_info = values.get('fields_info', False)
        if not fields_info:
            fields_info = {'id': False, 'display_name': False, 'write_date': True}
        fields_get = obj.fields_get()
        res = {}
        val_obj = {}
        items = []
        for field in fields_info.keys():
            f_obj = fields_get[field]
            string = fields_get[field]['string']
            field_value = obj[field]
            if f_obj['type'] in ['many2many', 'one2many']:
                field, list_ids = field_value.m2m_dict(obj[field])
                val_obj[string] = field
                val_obj['{}_list_ids'.format(field['string'])] = list_ids
            elif f_obj['type'] == 'many2one':
                val_obj[string] = field_value.m2o_dict(field_value)
            elif f_obj['type'] in ['datetime', 'date']:
                val_obj[string] = field_value.strftime('%d-%m')
            elif f_obj['type'] == 'selection':
                val_obj[string] = self.selection_dict(f_obj, field_value)
            else:
                val_obj[string] = field_value
            new_key = {'name': string, 'value': val_obj[string], 'show': fields_info[field]}
            items.append(new_key)

        res['items'] = items
        res['image'] = False

        print("\n MODAL: ---------------------------")
        pprint.PrettyPrinter(indent=2).pprint(res)
        return res


    @api.model
    def get_apk_object(self, values):

        model = values.get('model', False)
        id = values.get('id', False)
        if id:
            id = int(id)
            res = self.env[model].browse(id).get_model_object(values)
        else:
            res = self.env[model].get_model_object(values)
        message = values.get('message')
        if message:
            res['message'] = '{}</br>{}'.format(res.get('message', ''), message)
        return res

    def get_model_object(self, values={}):
        ##ESTA FUNCION NO ERA VIABLE, ES MUY LENTA
        domain = values.get('domain', [])
        offset = values.get('offset', 0)
        limit = values.get('limit', 0)
        model = values.get('model', self._name)
        view = values.get('view', 'tree')
        order = values.get('order', False)
        if not self:
            model_id = self.env[model]
            if not model: return []
            obj_ids = model_id.search(domain, offset=offset, limit=limit, order=order)
        else:
            obj_ids = self
        vals = []
        if not obj_ids:
            return vals
        ## NUNCA DEBERÍA DE MOSTRAR DISTINTOS TIPOS DE PICKING_TYPE_ID ##
        ## Cojo aquí los campos a mostrar
        ## No tiene sentido quitar campos. Lo lógico es ponerlos o usarlo s que vienen por defecto
        ## Entonces el hide_fileds debe ser show_fields, asi solo llamo una vez
        ## print ("\n-----\nGET_APK_INFO {}: Ids = {}\n".format(model, obj_ids.ids))
        fields_list = []
        if model in ['stock.picking', 'stock.move', 'stock.move.line']:
            picking_type_id = obj_ids[0].picking_type_id
            if model == 'stock.picking':
                field = '{}_picking_fields'.format(view)
            if model == 'stock.move':
                field = '{}_move_fields'.format(view)
            if model == 'stock.move.line':
                field = '{}_move_line_fields'.format(view)
            if picking_type_id and picking_type_id[field]:
                fields_list = picking_type_id.group_code[field].split(",") or []
        if not fields_list:
            fields_list = values.get('fields', self.env[model].return_fields(view))
        fields_get = obj_ids.fields_get()
        for obj in obj_ids:

            val_obj = {}
            for field in fields_list:
                f_obj = fields_get[field]
                field_value = obj[field]
                if f_obj['type'] in ['many2many', 'one2many']:
                    value_ids, list_ids = field_value.m2m_dict(obj[field])
                    val_obj[field] = value_ids or []
                    val_obj['{}_list_ids'.format(field)] = list_ids
                elif f_obj['type'] == 'many2one':
                    val_obj[field] = field_value.m2o_dict(field_value)
                elif f_obj['type'] in ['datetime', 'date']:
                    val_obj[field] = field_value.strftime('%d %H:%M')
                elif f_obj['type'] == 'selection':
                    val_obj[field] = self.selection_dict(f_obj, field_value)
                else:
                    val_obj[field] = field_value
            vals.append(val_obj)
        if view == 'form' and vals:
            vals = vals[0]

        # print("\n VALORES: ---------------------------")
        # pprint.PrettyPrinter(indent=2).pprint(values)
        # print("\n REGISTRO: ---------------------------")
        # pprint.PrettyPrinter(indent=2).pprint(vals)
        # print("\n -------------------------------------")
        return vals

    @api.model
    def change_field_value(self, values):
        model = values.get('model')
        id = values.get('id')
        field = values.get('field')
        value = values.get('value')
        try:
            self.env[model].browse(id)[field] = value
            return [{field: value}]
        except:
            raise ValueError('error al escribir {} en el campo {}. Model {}. Id {}'.format(model, id, field, value))
        return


    @api.model
    def get_field_group(self, values):
        ## Función para obtener campos de filtro
        model = values['model']
        field = values['field']
        if values['type'] == 'Selection':
            selection_ids = self.env[model].fields_get()[field]['selection']
            vals = []
            for selection in selection_ids:
                vals += [{'value': selection[0], 'name': selection[1]}]
        if values['type'] == 'Many2one':
            model_dest = self.env[model].fields_get()[field]['relation']
            ids = [x[field][0] for x in self.env[model].read_group([], [field],[field])]
            vals = self.env[model_dest].search_read([('id', 'in', ids)], ['id', 'apk_name'])
        pprint.PrettyPrinter(indent=2).pprint(vals)
        return vals

class StockMove(models.Model):

    _inherit = ['info.apk', 'stock.move']
    _name = 'stock.move'


class StockQuant(models.Model):
    _name = 'stock.quant'
    _inherit = ['info.apk', 'stock.quant']

    def return_fields(self, mode='tree'):
        return ['id', 'product_id', 'reserved_quantity', 'quantity', 'location_id', 'lot_id', 'package_id']

class StockQuantPackage(models.Model):
    _name = 'stock.quant.package'
    _inherit = ['info.apk', 'stock.quant.package']

    def return_fields(self, mode='tree'):
        return ['id', 'apk_name', 'packaging_id']

class StockProductionLot(models.Model):
    _name = 'stock.production.lot'
    _inherit = ['info.apk', 'stock.production.lot']

    def return_fields(self, mode='tree'):
        return ['apk_name', 'ref']

class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = ['res.company', 'info.apk']

class ProductUom(models.Model):
    _name = 'uom.uom'
    _inherit = ['info.apk', 'uom.uom']

class StockWarehouse(models.Model):
    _name = 'stock.warehouse'
    _inherit = ['info.apk', 'stock.warehouse']

    def return_fields(self, mode='tree'):
        return ['id', 'name', 'code']

class ProductCategory(models.Model):
    _name = 'product.category'
    _inherit = ['info.apk', 'product.category']

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['info.apk', 'res.partner']

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.commercial_partner_id.name

