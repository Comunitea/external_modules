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
from openerp.osv import osv
from openerp.tools.translate import _

class merge_sales_forecast(osv.osv_memory):
    _name = "merge.sales.forecast"
    _description = "Sales Forecast Merge"

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        """
         Changes the view dynamically
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: New arch of view.
        """
        if context is None:
            context={}
        res = super(merge_sales_forecast, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar,submenu=False)
        if context.get('active_model','') == 'sales.forecast' and len(context['active_ids']) < 2:
            raise osv.except_osv(_('Warning'),
            _('Please select multiple sales forecasts to merge in the list view.'))
        return res

    def merge_sales_forecast(self, cr, uid, ids, context=None):
        """
             To merge similar type of sales forecasts.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: sales forecast view

        """
        sales_obj = self.pool.get('sales.forecast')
        #proc_obj = self.pool.get('procurement.order')
        mod_obj =self.pool.get('ir.model.data')
        if context is None:
            context = {}
        result = mod_obj._get_id(cr, uid, 'sales_forecast', 'view_sales_forecast_filter')
        id = mod_obj.read(cr, uid, result, ['res_id'])

        allorder = sales_obj.do_merge(cr, uid, context.get('active_ids',[]), context)

        return {
            'domain': "[('id','=',%d)]" % allorder,
            'name': _('Sales Forecasts'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sales.forecast',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'search_view_id': id['res_id']
        }

merge_sales_forecast()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
