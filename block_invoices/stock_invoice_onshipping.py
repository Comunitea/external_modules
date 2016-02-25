# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    @author Alberto Luengo Cabanillas
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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class stock_invoice_onshipping(osv.osv_memory):
    """

    """

    _inherit = 'stock.invoice.onshipping'

    def view_init(self, cr, uid, fields_list, context=None):
        """
        Herencia del metodo que carga la vista del formulario para añadir control
        sobre la facturacion a clientes bloqueados
        """
        pick_facade = self.pool.get('stock.picking')
        active_ids = context.get('active_ids',[])
        for pick in pick_facade.browse(cr, uid, active_ids, context=context):
            #Compruebo la empresa actual y su padre...
            partner_ids_to_check = [pick.partner_id and pick.partner_id.commercial_partner_id and pick.partner_id.commercial_partner_id.id or False, pick.partner_id and pick.partner_id.id or False]
            unique_partner_ids_to_check = filter(lambda a: a != False,[x for i,x in enumerate(partner_ids_to_check)if x not in partner_ids_to_check[i+1:]])
            for partner_id in unique_partner_ids_to_check:
                partner_fields_dict = self.pool.get('res.partner').read(cr, uid, partner_id, ['blocked_sales','name'])
                if partner_fields_dict['blocked_sales'] and pick.sale_id and not pick.sale_id.allow_confirm_blocked:
                    title = _("Warning for %s") % partner_fields_dict['name']
                    message = _('Customer blocked by lack of payment. Check the maturity dates of their account move lines.')
                    raise osv.except_osv(title, message)

        return super(stock_invoice_onshipping,self).view_init(cr, uid, fields_list, context=context)
