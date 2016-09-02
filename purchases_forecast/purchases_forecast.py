# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2012 Pexego Sistemas Informáticos All Rights Reserved
#    $Marta Vázquez Rodríguez$ <marta@pexego.es>
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
from openerp.osv import osv, fields
import time
from openerp import netsvc
from openerp.tools.translate import _

class purchases_forecast(osv.osv):

    _name = 'purchases.forecast'
    _description = 'Purchases forecast'
    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'analytic_id': fields.many2one('account.analytic.account', 'Account'),
        'commercial_id': fields.many2one('res.users', 'Commercial'),
        'date': fields.date('Date'),
        'purchases_forecast_lines': fields.one2many('purchases.forecast.line',
                                                'purchases_forecast_id', 'Lines'),
        'company_id': fields.many2one('res.company', 'Company'),
        'state': fields.selection([
                                ('draft','Draft'),
                                ('done', 'Done'),
                                ('approve', 'Approved'),
                                ('cancel', 'Cancel')], string="State",
                                required=True, readonly=True),
        'merged_into_id': fields.many2one('purchases.forecast', 'Merged into', required=False, readonly=True),
        'merged_from_ids': fields.one2many('purchases.forecast', 'merged_into_id', 'Merged from', readonly=True),
        'year': fields.integer('Year', size=4)

    }
    _defaults = {
        'state': 'draft',
        'commercial_id': lambda obj, cr, uid, context: uid,
    }

    def action_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'done'})
        return True

    def action_validate(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'approve'})
        return True

    def action_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def do_merge(self, cr, uid, ids, context=None):
        """
        To merge similar type of purchase orders.
        Orders will only be merged if:
        * Purchase Orders are in draft
        * Purchase Orders belong to the same partner
        * Purchase Orders are have same stock location, same pricelist
        Lines will only be merged if:
        * Order lines are exactly the same except for the quantity and unit

         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param ids: the ID or list of IDs
         @param context: A standard dictionary

         @return: new purchase order id

        """
        #TOFIX: merged order line should be unlink
        wf_service = netsvc.LocalService("workflow")
        forecast_obj = self.pool.get('purchases.forecast')
        forecast_line_obj = self.pool.get('purchases.forecast.line')
        product_obj = self.pool.get('product.product')
        old_ids = []
        res = {}
        lines = []
        company = self.pool.get('res.users').browse(cr, uid, uid).company_id and self.pool.get('res.users').browse(cr, uid, uid).company_id.id or False
        new_id = forecast_obj.create(cr, uid, {'name': _('Purchases forecast MERGED. '),
                                                   #'analytic_id': cur.analytic_id.id,
                                                   'commercial_id': uid,
                                                   'date': time.strftime('%d-%m-%Y'),
                                                   'company_id': company,
                                                   'state': 'draft'
                                                    })

        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        for porder in self.browse(cr, uid, ids, context=context):
            forecast_obj.write(cr, uid, porder.id,{'merged_into_id': new_id})
            old_ids.append(porder.id)
            for l in porder.purchases_forecast_lines:
                lines.append(l.id)
        if lines:
            for line in forecast_line_obj.browse(cr, uid, lines):
                if not res.get(line.product_id.id):
                    res[line.product_id.id] = {}
                for month in range(0,12):
                    if not res[line.product_id.id].get(months[month] + '_qty'):
                        res[line.product_id.id][months[month] + '_qty'] = 0.0
                    res[line.product_id.id][months[month] + '_qty'] = res[line.product_id.id][months[month] + '_qty'] + (eval('o.' + (months[month] + '_qty'),{'o': line}))

        if res:
            for product in res:
                nwline = forecast_line_obj.create(cr, uid, {
                                'purchases_forecast_id': new_id,
                                'actual_cost': product_obj.browse(cr, uid, product).standard_price,
                                'product_id': product})
                for month in range(0,12):
                    forecast_line_obj.write(cr, uid, nwline, {
                               months[month] + '_qty': res[product][months[month] + '_qty'],
                               months[month] + '_amount_total': res[product][months[month] + '_qty'] * product_obj.browse(cr, uid, product).standard_price})

            # make triggers pointing to the old purchases forecast to the new forecast
        if old_ids:
            for old_id in old_ids:
                wf_service.trg_validate(uid, 'purchases.forecast', old_id, 'action_cancel', cr)
        return new_id


class purchases_forecast_line(osv.osv):

    _name = 'purchases.forecast.line'
    _description = 'Purchases forecast lines'

    def _get_total_amount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.jan_amount_total + line.feb_amount_total + line.mar_amount_total + \
                           line.apr_amount_total + line.may_amount_total + line.jun_amount_total + \
                           line.jul_amount_total + line.aug_amount_total + line.sep_amount_total + \
                           line.oct_amount_total + line.nov_amount_total + line.dec_amount_total
        return res

    def _get_total_qty(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.jan_qty + line.feb_qty + line.mar_qty + \
                           line.apr_qty + line.may_qty + line.jun_qty + \
                           line.jul_qty + line.aug_qty + line.sep_qty + \
                           line.oct_qty + line.nov_qty + line.dec_qty
        return res

    def _get_actual_stock(self, cr, uid, ids, name, arg, context=None):
        res = {}
        c = context.copy()
        for line in self.browse(cr, uid, ids, context=context):
            c.update({'to_date': time.strftime('%Y-%m-%d %H:%M:%S')})
            res[line.id] = self.pool.get('product.product').browse(cr, uid, line.product_id.id, context=c).qty_available

        return res
    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'purchases_forecast_id': fields.many2one('purchases.forecast', 'Purchases forecast',
                                                required=True, ondelete='cascade'),
        'product_id': fields.many2one('product.product', 'Product',
                                        required=True),
        'actual_stock': fields.function(_get_actual_stock, type="float",
                                    digits=(16,2), string="Actual Stock", readonly=True),
        'actual_cost':fields.float('Cost €'),
        'jan_qty': fields.float('Qty'),

        'jan_amount_total': fields.float('Total €', digits=(16,2)),
        'feb_qty': fields.float('Qty'),

        'feb_amount_total': fields.float('Total €', digits=(16,2)),
        'mar_qty': fields.float('Qty'),

        'mar_amount_total': fields.float('Total €', digits=(16,2)),
        'apr_qty': fields.float('Qty'),

        'apr_amount_total': fields.float('Total €', digits=(16,2)),
        'may_qty': fields.float('Qty'),

        'may_amount_total': fields.float('Total €', digits=(16,2)),
        'jun_qty': fields.float('Qty'),

        'jun_amount_total': fields.float('Total €', digits=(16,2)),
        'jul_qty': fields.float('Qty'),

        'jul_amount_total': fields.float('Total €', digits=(16,2)),
        'aug_qty': fields.float('Qty'),

        'aug_amount_total': fields.float('Total €', digits=(16,2)),
        'sep_qty': fields.float('Qty'),

        'sep_amount_total': fields.float('Total €', digits=(16,2)),
        'oct_qty': fields.float('Qty'),

        'oct_amount_total': fields.float('Total €', digits=(16,2)),
        'nov_qty': fields.float('Qty'),

        'nov_amount_total': fields.float('Total €', digits=(16,2)),
        'dec_qty': fields.float('Qty'),

        'dec_amount_total': fields.float('Total €', digits=(16,2)),
        'total_qty': fields.function(_get_total_qty, type="float",
                                    digits=(16,2), string="Total Qty.", readonly=True),
        'total_amount': fields.function(_get_total_amount, type="float",
                                    digits=(16,2), string="Total €", readonly=True, store=True),
    }
    _defaults = {
        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'purchases.forecast.line') or '/'
    }



    def on_change_qty(self, cr, uid, ids, qty=0.0, field='', product_id=False, context=None):
        if context is None:
            context = {}

        res = {}
#
#        if amount and field != '' and product_id:
#            product_obj = self.pool.get('product.product').browse(cr, uid, product_id)
#            #TODO al cambiar la cantidad rellenar los € según tarifa
#            res[field + '_amount'] = 0.0

        return {'value': res}
