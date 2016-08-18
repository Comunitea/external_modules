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
from openerp import netsvc
import time
from openerp.tools.translate import _

class sales_forecast(osv.osv):

    _name = 'sales.forecast'
    _description = 'Sales forecast'
    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'analytic_id': fields.many2one('account.analytic.account', 'Account'),
        'commercial_id': fields.many2one('res.users', 'Commercial'),
        'date': fields.date('Date'),
        'sales_forecast_lines': fields.one2many('sales.forecast.line',
                                                'sales_forecast_id', 'Lines'),
        'company_id': fields.many2one('res.company', 'Company'),
        'state': fields.selection([
                                ('draft','Draft'),
                                ('done', 'Done'),
                                ('approve', 'Approved'),
                                ('cancel', 'Cancel')], string="State",
                                required=True, readonly=True),
        'pricelist_id': fields.many2one('product.pricelist', 'Pricelist'),
        'is_merged': fields.boolean('Is Merged', readonly=True, states={'draft': [('readonly', False)]},
                                    help="When this field is checked, the price list will not be used for calculating the amounts.",),
        'merged_into_id': fields.many2one('sales.forecast', 'Merged into', required=False, readonly=True),
        'merged_from_ids': fields.one2many('sales.forecast', 'merged_into_id', 'Merged from', readonly=True),
        'year': fields.integer('Year', size=4)
    }
    _defaults = {
        'state': 'draft',
        'commercial_id': lambda obj, cr, uid, context: uid,
        'is_merged': False,
    }

    def action_done(self, cr, uid, ids, context=None):
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
            'sep', 'oct', 'nov', 'dec']
        if context is None:
            user = self.pool.get('res.users').browse(cr, uid, uid, context)
            context = {
                'lang': user.context_lang
            }

        for o in self.browse(cr, uid, ids, context=context):

            if o.sales_forecast_lines and o.pricelist_id:
                pricelist_version_ids = self.pool.get('product.pricelist.version').search(cr, uid, [
                                                        ('pricelist_id', '=', o.pricelist_id.id),
                                                        '|',
                                                        ('date_start', '=', False),
                                                        ('date_start', '<=', o.date),
                                                        '|',
                                                        ('date_end', '=', False),
                                                        ('date_end', '>=', o.date),
                                                    ])

                if not pricelist_version_ids:
                    raise osv.except_osv(_('Warning !'), _("The pricelist has no active version !\nPlease create or activate one."))
                products_version = []
                if self.pool.get('product.pricelist.version').browse(cr, uid, pricelist_version_ids[0]).items_id:
                    for item in self.pool.get('product.pricelist.version').browse(cr, uid, pricelist_version_ids[0]).items_id:
                        if item.product_id:
                            products_version.append(item.product_id.id)
                    for line in o.sales_forecast_lines:
                        if not line.product_id.id in products_version:
                            raise osv.except_osv(_('Warning !'), _("The product [%s] %s is not in the selected pricelist !") % (line.product_id.default_code, line.product_id.name))
                        for m in range(0,12):
                            qty = (eval('o.' + (months[m] + '_qty'),{'o': line}))
                            price = self.pool.get('product.pricelist').price_get(cr, uid, [o.pricelist_id.id],
                            line.product_id.id, qty or 1.0, None, {
                                'uom': line.product_id.uom_id.id,
                                'date': o.date,
                                })[o.pricelist_id.id]
                            if price:
                                price_total = qty * price
                                self.pool.get('sales.forecast.line').write(cr, uid, line.id, {months[m] + '_amount': price_total})

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
        forecast_obj = self.pool.get('sales.forecast')
        forecast_line_obj = self.pool.get('sales.forecast.line')
        product_obj = self.pool.get('product.product')
        old_ids = []
        res = {}
        lines = []
        company = self.pool.get('res.users').browse(cr, uid, uid).company_id and self.pool.get('res.users').browse(cr, uid, uid).company_id.id or False
        new_id = forecast_obj.create(cr, uid, {'name': _('Sales forecast MERGED. '),
                                                   #'analytic_id': cur.analytic_id.id,
                                                   'commercial_id': uid,
                                                   'date': time.strftime('%d-%m-%Y'),
                                                   'company_id': company,
                                                   'state': 'draft',
                                                   'is_merged': 'True',
                                                    })

        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        for porder in self.browse(cr, uid, ids, context=context):
            forecast_obj.write(cr, uid, porder.id,{'merged_into_id': new_id})
            old_ids.append(porder.id)
            for l in porder.sales_forecast_lines:
                lines.append(l.id)
        if lines:
            for line in forecast_line_obj.browse(cr, uid, lines):
                if not res.get(line.product_id.id):
                    res[line.product_id.id] = {}
                for month in range(0,12):
                    if not res[line.product_id.id].get(months[month] + '_qty'):
                        res[line.product_id.id][months[month] + '_qty'] = 0.0
                        res[line.product_id.id][months[month] + '_amount'] = 0.0
                    res[line.product_id.id][months[month] + '_qty'] = res[line.product_id.id][months[month] + '_qty'] + (eval('o.' + (months[month] + '_qty'),{'o': line}))
                    res[line.product_id.id][months[month] + '_amount'] = res[line.product_id.id][months[month] + '_amount'] + (eval('o.' + (months[month] + '_amount'),{'o': line}))

        if res:
            for product in res:
                nwline = forecast_line_obj.create(cr, uid, {
                                'sales_forecast_id': new_id,
                                'actual_cost': product_obj.browse(cr, uid, product).standard_price,
                                'product_id': product})
                for month in range(0,12):
                    forecast_line_obj.write(cr, uid, nwline, {
                        months[month] + '_qty': res[product][months[month] + '_qty'],
                        months[month] + '_amount': res[product][months[month] + '_amount']})
                        #months[month] + '_amount_total': res[product][months[month] + '_qty'] * product_obj.browse(cr, uid, product).standard_price})

        # make triggers pointing to the old purchases forecast to the new forecast
        if old_ids:
            for old_id in old_ids:
                wf_service.trg_validate(uid, 'sales.forecast', old_id, 'action_cancel', cr)
        return new_id

    def write(self, cr, uid, ids, vals, context=None):
        """Modificación del método de escritura para que si la prevision tiene is_merged = True
           no guarde el valor de pricelist_id si es fijado"""
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]

        #Hacemos el cambio si ha fijado el pricelist_id y is_merged es true
        if vals.get('is_merged', False) :
            vals.update({'pricelist_id': False})
            vals.update({'budget_version_id': False})
            vals.update({'budget_item_id': False})

        return super(sales_forecast, self).write(cr, uid, ids, vals, context=context)


class sales_forecast_line(osv.osv):

    _name = 'sales.forecast.line'
    _description = 'Sales forecast lines'

    def _get_total_amount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.jan_amount + line.feb_amount + line.mar_amount + \
                           line.apr_amount + line.may_amount + line.jun_amount + \
                           line.jul_amount + line.aug_amount + line.sep_amount + \
                           line.oct_amount + line.nov_amount + line.dec_amount
        return res

    def _get_total_qty(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.jan_qty + line.feb_qty + line.mar_qty + \
                           line.apr_qty + line.may_qty + line.jun_qty + \
                           line.jul_qty + line.aug_qty + line.sep_qty + \
                           line.oct_qty + line.nov_qty + line.dec_qty
        return res

    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'sales_forecast_id': fields.many2one('sales.forecast', 'Sales forecast',
                                                required=True, ondelete='cascade'),
        'product_id': fields.many2one('product.product', 'Product',
                                        required=True),
        'jan_qty': fields.float('Qty', digits=(16,2)),
        'jan_amount': fields.float('€', digits=(16,2)),
        'feb_qty': fields.float('Qty', digits=(16,2)),
        'feb_amount': fields.float('€', digits=(16,2)),
        'mar_qty': fields.float('Qty', digits=(16,2)),
        'mar_amount': fields.float('€', digits=(16,2)),
        'apr_qty': fields.float('Qty', digits=(16,2)),
        'apr_amount': fields.float('€', digits=(16,2)),
        'may_qty': fields.float('Qty', digits=(16,2)),
        'may_amount': fields.float('€', digits=(16,2)),
        'jun_qty': fields.float('Qty', digits=(16,2)),
        'jun_amount': fields.float('€', digits=(16,2)),
        'jul_qty': fields.float('Qty', digits=(16,2)),
        'jul_amount': fields.float('€', digits=(16,2)),
        'aug_qty': fields.float('Qty', digits=(16,2)),
        'aug_amount': fields.float('€', digits=(16,2)),
        'sep_qty': fields.float('Qty', digits=(16,2)),
        'sep_amount': fields.float('€', digits=(16,2)),
        'oct_qty': fields.float('Qty', digits=(16,2)),
        'oct_amount': fields.float('€', digits=(16,2)),
        'nov_qty': fields.float('Qty', digits=(16,2)),
        'nov_amount': fields.float('€', digits=(16,2)),
        'dec_qty': fields.float('Qty', digits=(16,2)),
        'dec_amount': fields.float('€', digits=(16,2)),
        'total_qty': fields.function(_get_total_qty, type="float",
                                    digits=(16,2), string="Total Qty.", readonly=True, store=True),
        'total_amount': fields.function(_get_total_amount, type="float",
                                    digits=(16,2), string="Total €", readonly=True, store=True),
    }
    _defaults = {
        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'sales.forecast.line') or '/'
    }

    def on_change_amount(self, cr, uid, ids, amount=0.0, field='', product_id=False, context=None):
        if context is None:
            context = {}

        res = {}

#        if amount and field != '' and product_id:
#            product_obj = self.pool.get('product.product').browse(cr, uid, product_id)
#            #TODO al cambiar los € rellenar la cantidad según tarifa
#            res[field + '_qty'] = 0.0

        return {'value': res}

    def on_change_qty(self, cr, uid, ids, qty=0.0, field='', product_id=False, context=None):
        if context is None:
            context = {}

        res = {}

#        if amount and field != '' and product_id:
#            product_obj = self.pool.get('product.product').browse(cr, uid, product_id)
#            #TODO al cambiar la cantidad rellenar los € según tarifa
#            res[field + '_amount'] = 0.0

        return {'value': res}
