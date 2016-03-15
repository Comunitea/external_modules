# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009 Albert Cervera i Areny (http://www.nan-tic.com). All Rights Reserved
#    Copyright (c) 2011 Pexego Sistemas Informáticos. All Rights Reserved
#                       Alberto Luengo Cabanillas <alberto@pexego.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


""" Open Risk Window and show Partner relative information """

from openerp.osv import osv, fields
from openerp.tools.translate import _


RISK_STATUS = [('company_granted', 'Credit granted by the company'),
               ('insurance_granted', 'Credit granted by the insurance'),
               ('requested', 'Insurance requested'),
               ('request_again', 'Insurance credit should be requested again'),
               ('denied', 'Credit denied by the insurance company'),
               ('incidents', 'Customer with incidents at risk'),
               ('new_customer', 'Warning! New customer - See payments')]

class open_risk_window(osv.osv_memory):
    """ Open Risk Window and show Partner relative information """

    _name = "open.risk.window"
    _description = "Partner's risk information"

    _columns = {
        'unpayed_amount': fields.float('Expired Unpaid Payments', digits=(4,2), readonly="True"),
        'pending_amount': fields.float('Unexpired Unpaid Payments', digits=(4,2), readonly="True"),
        'draft_invoices_amount': fields.float('Draft Invoices', digits=(4,2), readonly="True"),
        'circulating_amount': fields.float('Payments Sent to Bank', digits=(4,2), readonly="True"), # Pedro field
        'pending_orders_amount': fields.float('Uninvoiced Orders', digits=(4,2), readonly="True"),
        'total_debt': fields.float('Total Debt', digits=(4,2), readonly="True"),
        'credit_limit': fields.float('Credit Limit', digits=(4,2), readonly="True"),
        'available_risk': fields.float('Available Credit', digits=(4,2), readonly="True"),
        'total_risk_percent': fields.float('Credit Usage (%)', digits=(4,2), readonly="True"),
        'risk_insurance_status': fields.selection(RISK_STATUS, 'Risk Status', readonly="True",
                                                  help="This option is used to define the risk status.\n" \
                                                  "Credit granted by the company: Only company's credit limit are applied.\n"\
                                                  "Credit granted by the insurance: Only insurance's credit limit are applied.\n"\
                                                  "Insurance requested: The risk has been requested to the insurance company.\n"\
                                                  "Insurance credit should be requested again: The risk should be requested again to the insurance company.\n"\
                                                  "Credit denied by the insurance company: The insurance company has denied the risk.\n"\
                                                  "Customer with incidents at risk: The customer have incidents at risk.\n"\
                                                  "Warning! New customer - See payments: New customer. Track payments."),
        'risk_insurance_notes': fields.text('Notes', readonly="True"),
        }

    _defaults = {
        'unpayed_amount': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr,uid,context['risk_partner_id'],context).unpayed_amount or 0.0,
        'pending_amount': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr,uid,context['risk_partner_id'],context).pending_amount or 0.0,
        'draft_invoices_amount': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr,uid,context['risk_partner_id'],context).draft_invoices_amount or 0.0,
        'circulating_amount': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr, uid, context['risk_partner_id'], context).circulating_amount or 0.0, # Pedro field
        'pending_orders_amount': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr,uid,context['risk_partner_id'],context).pending_orders_amount or 0.0,
        'total_debt': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr,uid,context['risk_partner_id'],context).total_debt or 0.0,
        'credit_limit': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr,uid,context['risk_partner_id'],context).credit_limit or 0.0,
        'available_risk': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr,uid,context['risk_partner_id'],context).available_risk or 0.0,
        'total_risk_percent': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr,uid,context['risk_partner_id'],context).total_risk_percent or 0.0,
        'risk_insurance_status': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr, uid, context['risk_partner_id'], context).risk_insurance_status or '',
        'risk_insurance_notes': lambda self, cr, uid, context: self.pool.get('res.partner').browse(cr, uid, context['risk_partner_id'], context).risk_insurance_notes or '',
    }

    # From Pedro Module.
    def default_get(self, cr, uid, fields, context=None):
        """ Get default values
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param fields: List of fields for default value
        @param context: A standard dictionary
        @return: default values of fields
        """
        if context is None:
            context = {}
        if not context.get('risk_partner_id', False):  # Si no trae el parametro se supone que se llama desde el cliente
            context.update({'risk_partner_id': context.get('active_id', False)})
        res = super(open_risk_window, self).default_get(cr, uid, fields,
                                                        context=context)
        return res
