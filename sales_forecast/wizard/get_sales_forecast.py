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

import calendar
import time

class get_sales_forecast(osv.osv_memory):

    _name = 'get.sales.forecast'
    _description = 'Preload a sales forecast'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'account_id': fields.many2one('account.analytic.account', 'Account',
                                        required=True),
        'percent_increase': fields.float('% Increase', digits=(16,2))
    }

    def get_sales_forecast(self, cr, uid, ids, context=None):
        """ Get forecast sales for the selected analytic account and,
                    which may also increase profits in the percentage selected."""


        if context is None:
            context = {}

        amount = 0.0

        new_id = False

        products = {}
        value = {}

        invoice_ids = []
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
            'sep', 'oct', 'nov', 'dec']

        inv_obj = self.pool.get('account.invoice')
        forecast_obj = self.pool.get('sales.forecast')
        forecast_line_obj = self.pool.get('sales.forecast.line')
        user_obj = self.pool.get('res.users')
        product_obj = self.pool.get('product.product')

        company_id = user_obj.browse(cr, uid, uid).company_id.id

        for form in self.browse(cr, uid, ids):
            #create forecast sales without lines
            new_id = forecast_obj.create(cr, uid, {'name': form.name,
                                                   'analytic_id': form.account_id.id,
                                                   'commercial_id': uid,
                                                   'date': time.strftime('%d-%m-%Y'),
                                                   'company_id': company_id,
                                                   'state': 'draft'
                                                    })
            for month in range(0,11):
                #I find all the invoices in for each month last year.
                domain =  \
                    [('date_invoice','>',str('01-' + str(month + 1) +
                        '-' + str(int(time.strftime('%d-%m-%Y')[6:]) - 1))),
                    ('date_invoice','<',
                        str((calendar.monthrange((int(time.strftime('%d-%m-%Y')[6:]) - 1),
                        (month + 1))[1])) + '-' + str(month + 1) + '-' +
                        str(int(time.strftime('%d-%m-%Y')[6:]) - 1)),
                    ('company_id','=', company_id)]

                invoice_ids = inv_obj.search(cr, uid, domain)
                if invoice_ids:

                    #If invoices, step through lines that share the selected
                    #analytic account and save them in a dictionary, with the
                    #id of product of the line like key:
                    #{Product_Id: [(amount, benefits)]}
                    for inv in inv_obj.browse(cr, uid, invoice_ids):
                        for line in inv.invoice_line:
                            if line.account_analytic_id and \
                                    line.account_analytic_id.id == form.account_id.id and \
                                    line.product_id:

                                quantity = self.pool.get('product.uom')._compute_qty(cr, uid, line.uos_id.id,line.quantity, line.product_id.uom_id.id)
                                if products.get(line.product_id.id):
                                    new_val = (products[line.product_id.id][0][0] + quantity,
                                               products[line.product_id.id][0][1] + line.price_subtotal)
                                    products[line.product_id.id][0] = new_val
                                else:
                                    products[line.product_id.id] = []
                                    products[line.product_id.id].append((quantity,
                                                                    line.price_subtotal))
                    if products:
                        for product in products:
                            if form.percent_increase:
                                #Calculation percentage increase
                                qty = products[product][0][0] + \
                                    ((form.percent_increase / 100) * \
                                    products[product][0][0])
                            else:
                                qty = products[product][0][0]

                            cur_forecast = forecast_obj.browse(cr, uid, new_id)
                            l_products = forecast_line_obj.search(cr, uid,
                                [('product_id','=', product),
                                ('sales_forecast_id', '=', cur_forecast.id)])
                            #If there are already lines created for the same product,
                            #update the quantities. Else, I create a new line
                            if l_products:
                                l = forecast_line_obj.browse(cr, uid, l_products[0])
                                if l.product_id.id == product:
                                    forecast_line_obj.write(cr, uid, l.id,
                                        {months[month] + '_qty': (qty + \
                                        (eval('o.' + (months[month] + '_qty'),{'o': l})))})
                            else:
                                forecast_line_obj.create(cr, uid, {
                                    'sales_forecast_id': new_id,
                                    'product_id': product,
                                    months[month] + '_qty': qty})

                        products = {}

        value = {
                'domain': str([('id', 'in', [new_id])]),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sales.forecast',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'res_id': new_id
                }

        return value

get_sales_forecast()
