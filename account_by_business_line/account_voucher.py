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

class account_voucher(orm.Model):

    _inherit = "account.voucher"

    _columns = {
        'business_line_id': fields.many2one('account.business.line', 'Write-Off Business line')
    }

    def writeoff_move_line_get(self, cr, uid, voucher_id, line_total, move_id, name, company_currency, current_currency, context=None):
        if context is None: context = {}
        move_line = super(account_voucher, self).writeoff_move_line_get(cr, uid, voucher_id, line_total, move_id, name, company_currency, current_currency, context=context)
        if move_line:
            voucher_brw = self.pool.get('account.voucher').browse(cr,uid,voucher_id,context)
            move_line['business_line_id'] = voucher_brw.business_line_id and voucher_brw.business_line_id.id or False

        return move_line

