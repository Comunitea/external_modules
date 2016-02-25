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

from openerp.osv import orm


class sale_order_line(orm.Model):

    _inherit = "sale.order.line"

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):

        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product,
                                                             qty=qty, uom=uom, qty_uos=qty_uos,
                                                             uos=uos, name=name, partner_id=partner_id,
                                                             lang=lang, update_tax=update_tax, date_order=date_order,
                                                             packaging=packaging, fiscal_position=fiscal_position, flag=flag,
                                                             context=context)
        if partner_id and product and res.get('value'):
            context = context or {}
            customer_name_ids = self.pool.get('customer.product.name').search(cr, uid, [('product_id', '=', product),('partner_id', '=', partner_id)])
            if customer_name_ids:
                customer_name = self.pool.get('customer.product.name').browse(cr, uid, customer_name_ids[0])
                res['value']['name'] = customer_name.name

        return res
