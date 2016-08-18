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
from openerp.tools.translate import _

class scale_sales_forecast(osv.osv_memory):
    _name = "scale.sales.forecast"
    _description = "Preload a scale sales forecast"
    _columns = {
        'percent_increase': fields.float('% Increase', digits=(16,2))
    }

    def scale_sales_forecast(self, cr, uid, ids, context=None):
        default = {}
        context = context or {}
        new_ids = []
        if not ids:
            return
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
            'sep', 'oct', 'nov', 'dec']

        if context.get('active_ids', []):
            forecast_obj = self.pool.get('sales.forecast')
            forecast_line_obj = self.pool.get('sales.forecast.line')
            for reg_id in context['active_ids']:
                reg_original = forecast_obj.browse(cr, uid, reg_id)
                val_percent_increase = self.browse(cr, uid, ids)[0].percent_increase

                default.update({'name' : reg_original.name + ' SCALED ' + str(val_percent_increase) + '%'})
                default.update({'purchase_forecast_id': False})
                default.update({'sales_forecast_lines': False})
                
                new_id = forecast_obj.copy(cr, uid, reg_id, default, context)

                new_ids.append(new_id)

                o = forecast_obj.browse(cr, uid, reg_id)
                
                for line in o.sales_forecast_lines:
                    default = {}
                    default.update({'sales_forecast_id': new_id})
                    for m in range(0,12):
                        qty = (eval('o.' + (months[m] + '_qty'),{'o': line}))
                        qty = qty * (1 + (val_percent_increase / 100))
                        default.update({months[m] + '_qty': qty})
                        default.update({months[m] + '_amount': 0})
                    new_id2 = forecast_line_obj.copy(cr, uid, line.id, default, context)
                    
        mod_obj =self.pool.get('ir.model.data')
        res1 = mod_obj.get_object_reference(cr, uid, 'sales_forecast', 'view_sales_forecast_form')
        res2 = mod_obj.get_object_reference(cr, uid, 'sales_forecast', 'view_sales_forecast_filter')

        if len(context.get('active_ids', [])) == 1:
            result = {
                    'name': _('Sales Forecasts'),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sales.forecast',
                    'view_id': res1 and res1[1] or False,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'current',
                    'res_id': new_ids and new_ids[0] or False,
                    }
        elif len(context.get('active_ids', [])) > 1:
            result = {
                    'domain': [('id','in',new_ids)],
                    'name': _('Sales Forecasts'),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'sales.forecast',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'search_view_id': res2 and res2[1] or False
                    }
        else:
            result = {'type':'ir.actions.act_window_close'}

        return result

scale_sales_forecast()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
