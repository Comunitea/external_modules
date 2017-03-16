# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
import time
from datetime import date, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    chanel = fields.Selection([('erp', 'ERP'),
                               ('telesale', 'Telesale')],
                              string='Is a telesale order',
                              default='erp',
                              readonly=True)
    date_planned = fields.Datetime('Date Planed')

    @api.model
    def create_order_from_ui(self, orders):
        t_partner = self.env['res.partner']
        t_order = self.env['sale.order']
        t_order_line = self.env['sale.order.line']
        t_product = self.env['product.product']

        order_ids = []

        for rec in orders:
            order = rec['data']
            order_obj = False
            # if order['erp_id'] and order['erp_state'] != 'draft':

            #     self.cancel_sale_to_draft(cr, uid, order['erp_id'], context)
            #     order['erp_state'] = 'draft'

            partner_obj = t_partner.browse(order['partner_id'])

            vals = {
                # 'name': '/',
                'partner_id': partner_obj.id,
                'pricelist_id': partner_obj.property_product_pricelist.id,
                'partner_invoice_id': partner_obj.id,
                'partner_shipping_id': partner_obj.id,
                'chanel': 'telesale',
                'order_policy': 'picking',
                'date_order': time.strftime("%Y-%m-%d %H:%M:%S"),
                'date_planned': order['date_planned'] + " 19:00:00" or False,
                'note': order['note']
            }
            if order['erp_id'] and order['erp_state'] == 'draft':
                order_obj = t_order.browse(order['erp_id'])
                order_obj.write(vals)
            else:
                # vals['name'] = '/'
                order_obj = t_order.create(vals)

            order_ids.append(order_obj.id)

            order_lines = order['lines']

            if order['erp_id'] and order['erp_state'] == 'draft':
                domain = [('order_id', '=', order_obj.id)]
                line_objs = t_order_line.search(domain)
                line_objs.unlink()
            for line in order_lines:
                product_obj = t_product.browse(line['product_id'])
                product_uom_id = line.get('product_uom', False)
                product_uom_qty = line.get('qty', 0.0)
                vals = {
                    'order_id': order_obj.id,
                    'name': product_obj.name,
                    'product_id': product_obj.id,
                    'price_unit': line.get('price_unit', 0.0),
                    'product_uom': product_uom_id,
                    'product_uom_qty': product_uom_qty,
                    'tax_id': [(6, 0, line.get('tax_ids', False))],
                    'discount': line.get('discount', 0.0),
                }
                t_order_line.create(vals)
            if order['action_button'] == 'confirm':
                order_obj.action_button_confirm()
        return order_ids


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def ts_product_id_change(self, product_id, partner_id):
        res = {}

        order_t = self.env['sale.order']
        partner = self.env['res.partner'].browse(partner_id)

        order = order_t.new({'partner_id': partner_id,
                             'date_order': time.strftime("%Y-%m-%d"),
                             'pricelist_id':
                             partner.property_product_pricelist.id})
        line = self.new({'order_id': order.id,
                         'product_id': product_id})
        line.product_id_change()
        res.update({
            'price_unit': line.price_unit,
            'product_uom': line.product_uom.id,
            'product_uom_qty': line.product_uom_qty,
            'tax_id': [x.id for x in line.tax_id]

        })
        return res

    @api.model
    def get_last_lines_by(self, period, client_id):
        """
        """
        cr = self._cr
        date_str = date.today()
        if period == "ult":
            sq = """ SELECT id
                     FROM sale_order_line sol
                     WHERE order_id in
                        (SELECT id
                         FROM sale_order WHERE
                         state in ('sale','done')
                         and partner_id = %s order by id desc limit 1)
                    ORDER BY id desc"""

        else:
            if period == "3month":
                date_str = date.today() - timedelta(90)
            elif period == "year":
                date_str = date.today() - timedelta(365)
            date_str = date_str.strftime("%Y-%m-%d %H:%M:%S")
            sq = """ SELECT * FROM
                        (SELECT distinct on (product_id) sol.id
                         FROM sale_order_line sol
                         INNER JOIN sale_order so ON so.id = sol.order_id
                         WHERE so.state in
                            ('sale','done')
                         AND so.partner_id = %s
                         AND so.date_order >= %s
                         ORDER BY product_id desc, id desc) AS sq
                    ORDER BY id desc"""

        if period != 'ult':
            cr.execute(sq, (client_id, date_str))
        else:
            cr.execute(sq, (client_id,))
        fetch = cr.fetchall()
        prod_ids = [x[0] for x in fetch]
        res = []
        for l in self.browse(prod_ids):
            dic = {
                'product_id': (l.product_id.id, l.product_id.name),
                'price_unit': l.product_id.list_price,
                'default_code': l.product_id.default_code or
                l.product_id.default_code2
            }
            res.append(dic)
        # print "**************************************"
        # print res
        # print "**************************************"
        return res
