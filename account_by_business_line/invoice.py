# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013
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
from openerp import api


class account_invoice(orm.Model):

    _inherit = "account.invoice"

    _columns = {
        'business_line_id': fields.many2one('account.business.line', 'Business line')
    }

    def line_get_convert(self, cr, uid, x, part, date, context=None):
        res=super(account_invoice,self).line_get_convert(cr, uid, x, part, date, context=context)
        res['business_line_id'] = x.get('business_line_id', False)
        return res

    @api.model
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):
        vals = super(account_invoice, self)._prepare_refund(invoice, date=date,
                                                            period_id=period_id,
                                                            description=description,
                                                            journal_id=journal_id)
        vals["business_line_id"] = invoice.business_line_id.id
        return vals


class account_invoice_line(orm.Model):

    _inherit = "account.invoice.line"

    _columns = {
        'business_line_id': fields.many2one('account.business.line', 'Business line')
    }

    _defaults = {
        'business_line_id': lambda self,cr,uid,c: c.get('business_line', False)
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        data = super(account_invoice_line, self).default_get(cr, uid, fields, context=context)
        if context.get('business_line', False):
            data['business_line_id'] = context['business_line']

        return data

    def move_line_get_item(self, cr, uid, line, context=None):
        res = super(account_invoice_line, self).move_line_get_item(cr, uid, line, context=context)
        if res.get('account_id'):
            need_bussines_line = self.pool.get('account.account').browse(cr, uid, res['account_id']).need_business_line
            if need_bussines_line:
                res['business_line_id'] = line.business_line_id and line.business_line_id.id or (line.invoice_id.business_line_id and line.invoice_id.business_line_id.id or False)

        return res

