# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014
#    Pexego Sistemas Informáticos (http://www.pexego.es)
#    Copyright (C) 2015
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
#    $Omar Castiñeira Saavedra$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
import openerp.addons.decimal_precision as dp
import time


class product_supplierinfo(orm.Model):

    _inherit = "product.supplierinfo"

    def _get_supplier_currency(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None: context = {}
        for supp in self.browse(cr, uid, ids, context=context):
            res[supp.id] = supp.name.property_product_pricelist_purchase and supp.name.property_product_pricelist_purchase.currency_id.id or False

        return res

    _columns = {
        'supplier_currency_id': fields.function(_get_supplier_currency, method=True, string='Currency', readonly=True, type="many2one", relation="res.currency")
    }



class pricelist_partnerinfo(orm.Model):

    _inherit = 'pricelist.partnerinfo'

    _columns = {
        'from_date': fields.date('From date', required=True),
        'discount': fields.float('Discount', digits=(4,2), help="About 100"),
        'gross_amount': fields.float('Gross unit amount', digits_compute=dp.get_precision('Purchase Price')),
    }

    _defaults = {
        'from_date': lambda *a: time.strftime("%Y-%m-%d")
    }

    def on_change_price(self, cr, uid, ids, gross_amount, discount):
        res = {'value': {'price': gross_amount * (1-(discount or 0.0)/100.0)}}
        return res

