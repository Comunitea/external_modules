# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    @author Alberto Luengo Cabanillas
#    Copyright (C) 2015
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

from openerp.osv import fields, osv
from datetime import datetime,timedelta
import time

class ResPartner(osv.osv):
    """
    Herencia de la clase Empresa
    """

    def check_customer_blocked_sales(self, cr, uid, automatic=False,use_new_cursor=False, context=None):
        """
        Buscamos todos los asientos contables de aquellas facturas de cliente que no estén pagadas que posean una fecha de vencimiento
        anterior a la fecha actual+periodo de gracia configurable en la compañia...
        """
        move_line_facade = self.pool.get('account.move.line')
        account_facade = self.pool.get('account.account')
        partner_facade = self.pool.get('res.partner')
        blocked_partner_ids = []
        root_company_dict = self.pool.get('res.users').read(cr, uid,uid,['company_id'])
        root_company_id = root_company_dict['company_id'][0]
        company_dict = self.pool.get('res.company').read(cr, uid,root_company_id,['block_customer_days'])
        formatted_date = datetime.strptime(time.strftime('%Y-%m-%d'), "%Y-%m-%d")
        limit_customer_date = datetime.strftime(formatted_date + timedelta(days=-int(company_dict['block_customer_days'])),"%Y-%m-%d")

        #Buscamos efectos no conciliados, con fecha anterior a la fecha limite, de tipo 'receivable'
        cust_account_ids = account_facade.search(cr, uid, [('company_id','=',root_company_id),('type','=','receivable'),('code','like','430%')])
        move_line_ids = move_line_facade.search(cr, uid, [('account_id','in',cust_account_ids),('date_maturity','<',limit_customer_date),('reconcile_id','=',False)])
        if len(move_line_ids)>0:
            moves_to_search_dict = move_line_facade.read(cr, uid, move_line_ids,['partner_id'])
            for dict in moves_to_search_dict:
                if dict['partner_id'][0] not in blocked_partner_ids:
                    blocked_partner_ids.append(dict['partner_id'][0])

        #Bloqueamos todos los clientes de la anterior lista
        partner_facade.write(cr, uid, blocked_partner_ids,{'blocked_sales': True},context)
        #Empresas no bloqueadas: todas aquellas que no figuran en el listado de empresas bloqueadas
        all_customer_ids = partner_facade.search(cr, uid, [('customer','=',True),('company_id','=',root_company_id)])
        non_blocked_partner_ids = list(set(all_customer_ids) - set(blocked_partner_ids))
        partner_facade.write(cr, uid, non_blocked_partner_ids,{'blocked_sales': False},context)

        return

    def check_customer_block_state(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        account_facade = self.pool.get('account.account')
        move_line_facade = self.pool.get('account.move.line')
        user = self.pool.get('res.users').browse(cr, uid, uid)
        formatted_date = datetime.strptime(time.strftime('%Y-%m-%d'),
                                           "%Y-%m-%d")
        limit_customer_date = datetime.\
            strftime(formatted_date + timedelta(days=\
                -int(user.company_id.block_customer_days)),"%Y-%m-%d")
        for partner in self.browse(cr, uid, ids, context=context):
            cust_account_ids = account_facade.search(cr, uid,
                                                     [('company_id', '=',
                                                       user.company_id.id),
                                                      ('type', '=',
                                                       'receivable'),
                                                      ('code', 'like',
                                                       '430%')])
            move_line_ids = move_line_facade.search(cr, uid,
                                                    [('account_id', 'in',
                                                      cust_account_ids),
                                                     ('date_maturity', '<',
                                                      limit_customer_date),
                                                     ('reconcile_id', '=',
                                                      False),
                                                     ('partner_id', '=',
                                                      partner.id)])
            if move_line_ids:
                partner.write({'blocked_sales': True})
            else:
                partner.write({'blocked_sales': False})

        return True

    _inherit = "res.partner"
    _columns = {
        'blocked_sales': fields.boolean('Sales blocked?')
    }
