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

class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['info.apk', 'product.product']

    #tracking = fields.Selection(related='product_tmpl_id.tracking')
    wh_code = fields.Char(string='Unique WH Product Code',
                          help="Código univoco para identificar el producto en con la pistola: "
                               "Ean 13, Referencia interna, id, id de prestahsop ...")

    def return_fields(self, mode='tree'):
        return ['id', 'apk_name', 'default_code', 'list_price', 'qty_available', 'virtual_available', 'tracking', 'wh_code']

    def m2o_dict(self, field):
        if field:
            return {'id': field.id, 'name': field.apk_name, 'default_code': field.default_code, 'barcode': field.barcode, 'wh_code': field.wh_code}
        else:
            return {'id': False}

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            product_ids = []
            if operator in positive_operators:
                product_ids = self._search([('wh_code', '=', name)] + args, limit=limit,
                                           access_rights_uid=name_get_uid)
            if product_ids:
                return self.browse(product_ids).name_get()
        return super()._name_search(name=name, args=args, operator=operator, limit=100, name_get_uid=name_get_uid)
