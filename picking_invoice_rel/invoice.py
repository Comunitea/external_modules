# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011 ChriCar Beteiligungs- und Beratungs- GmbH (<http://www.camptocamp.com>).
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
from openerp.osv import fields, osv
from openerp import api


class account_invoice(osv.osv):
    _inherit = "account.invoice"

# FIXME -this is not used, because info is in account_invoice.name
    def _client_order_refs(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for inv in self.browse(cr, uid, ids, context):
            client_ref = '' 
            for ref in inv.sale_order_ids:
                if ref.client_order_ref:
                    if client_ref:
                        client_ref +='; '
                    client_ref += ref.client_order_ref
            result[inv.id] = client_ref
        return result

    _columns = {
        'picking_ids': fields.many2many('stock.picking', 'picking_invoice_rel', 'invoice_id', 'picking_id', 'Pickings' ),
        'sale_order_ids': fields.many2many('sale.order', 'sale_order_invoice_rel', 'invoice_id', 'order_id', 'Sale Orders', readonly=True, help="This is the list of sale orders linked to this invoice. "),
        'client_order_refs' : fields.function(_client_order_refs, method=True, string="Client Sale Orders Ref", type='char'),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'picking_ids':[],
            'sale_order_ids':[],
            })
        res = super(account_invoice, self).copy(cr, uid, id, default, context)
        invoice_id = self.pool.get('account.invoice').browse(cr, uid, [res], context)
        invoice_id.invoice_line.write({'stock_move_id': False})
        return res

    @api.model
    def _refund_cleanup_lines(self, lines):
        res = super(account_invoice, self)._refund_cleanup_lines(lines)
        if lines and lines[0]._name != 'account.invoice.line':
            return res
        for i, line in enumerate(lines):
            res[i][2]['stock_move_id'] = False
        return res

account_invoice()


class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"
    _columns = {
        'stock_move_id': fields.many2one('stock.move', 'Stock move')
    }
    
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({'stock_move_id': False})
        return super(account_invoice_line, self).copy(cr, uid, id, default, context)
