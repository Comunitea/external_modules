# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    @author Alberto Luengo Cabanillas
#    Copyright (C) 2016
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
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

from openerp.osv import orm, osv
from openerp import fields
from openerp.tools.translate import _

class account_invoice(osv.osv):
    """

    """
    _inherit = 'account.invoice'
    blocked = fields.Boolean(related='partner_id.blocked_sales', copy=False)
    allow_confirm_blocked = fields.Boolean('Allow confirm')


    def invoice_validate(self, cr, uid, ids, context=None):
        """
        Herencia de uno de los métodos de la actividad 'open' del workflow
        de facturas para controlar el bloqueo de ventas a clientes
        """
        for invoice in self.browse(cr, uid, ids, context):
            #Compruebo la empresa actual y su padre...
            partner_ids_to_check = [invoice.partner_id.commercial_partner_id and invoice.partner_id.commercial_partner_id.id or False, invoice.partner_id.id]
            unique_partner_ids_to_check = filter(lambda a: a != False,[x for i,x in enumerate(partner_ids_to_check)if x not in partner_ids_to_check[i+1:]])
            for part_id in unique_partner_ids_to_check:
                partner_fields_dict = self.pool.get('res.partner').read(cr, uid, part_id, ['blocked_sales','name'])
                if partner_fields_dict['blocked_sales'] and not invoice.allow_confirm_blocked:
                    title = _("Warning for %s") % partner_fields_dict['name']
                    message = _('Customer blocked by lack of payment. Check the maturity dates of their account move lines.')
                    raise osv.except_osv(title, message)
        return super(account_invoice, self).invoice_validate(cr, uid, ids, context=context)

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,
                            date_invoice=False, payment_term=False,
                            partner_bank_id=False, company_id=False,
                            context=None):
        if not partner_id:
            return {'value': {
            'account_id': False,
            'payment_term': False,
            }
        }
        warning = {}
        title = False
        message = False
        #Compruebo la empresa actual y su padre...
        partner_dict = self.pool.get('res.partner').read(cr, uid, partner_id,['commercial_partner_id'])
        partner_ids_to_check = [partner_dict['commercial_partner_id'][0], partner_id]
        unique_partner_ids_to_check = filter(lambda a: a != False,[x for i,x in enumerate(partner_ids_to_check)if x not in partner_ids_to_check[i+1:]])
        for part_id in unique_partner_ids_to_check:
            partner_fields_dict = self.pool.get('res.partner').read(cr, uid, part_id, ['blocked_sales','name'])
            if partner_fields_dict['blocked_sales']:
                title = _("Warning for %s") % partner_fields_dict['name']
                message = _('Customer blocked by lack of payment. Check the maturity dates of their account move lines.')
                warning = {
                    'title': title,
                    'message': message
                    }
                #return {'value': {'partner_id': False}, 'warning': warning}

        result =  super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id,date_invoice=date_invoice, payment_term=payment_term, partner_bank_id=partner_bank_id, company_id=company_id, context=context)
        if result.get('warning',False):
            warning['title'] = title and title +' & '+ result['warning']['title'] or result['warning']['title']
            warning['message'] = message and message + ' ' + result['warning']['message'] or result['warning']['message']

        return {'value': result.get('value',{}), 'warning':warning}
