# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
import time
from datetime import date, timedelta
# import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    chanel = fields.Selection([('erp', 'ERP'),
                               ('telesale', 'Telesale')],
                              string='Chanel',
                              default='erp',
                              readonly=True)
    observations = fields.Text('Observations')

    @api.model
    def get_head_order_vals(self, order):
        t_partner = self.env['res.partner']
        t_default = self.env['ir.default']
        partner_obj = t_partner.browse(order['partner_id'])
        warehouse_id = False
        default_value = t_default.get('sale.order', 'warehouse_id')

        if default_value:
            warehouse_id = int(default_value.value_unpickle)
        else:
            warehouse_id = self._default_warehouse_id() and \
                self._default_warehouse_id()[0].id or 1
        # TODO, BUSCAR VALORES POR DEFECTO WAREHOUSE ID SINO PONER EL DE LA
        # COMPAÑÍA
        pricelist_id = partner_obj.property_product_pricelist.id
        if order.get('pricelist_id', False):
            pricelist_id = order['pricelist_id']

        values = self.ts_onchange_partner_id(partner_obj.id)
        res = {
            # 'name': '/',
            'partner_id': partner_obj.id,
            'pricelist_id': pricelist_id,
            'partner_invoice_id': partner_obj.id,
            'partner_shipping_id': order.get('partner_shipping_id',
                                             partner_obj.id),
            # 'order_policy': 'picking',
            'date_order': time.strftime("%Y-%m-%d %H:%M:%S"),
            # 'expected_date': order['expected_date'] + " 19:00:00" or
            # False,
            'note': order['note'],
            'observations': order['observations'],
            'warehouse_id': warehouse_id,
            'client_order_ref': order.get('client_order_ref', False),
            'fiscal_position_id': values.get('fiscal_position_id', False),
            'payment_term_id': values.get('payment_term_id', False),
            'payment_mode_id': values.get('payment_mode_id', False)
        }
        return res

    @api.model
    def create_order_from_ui(self, orders):
        t_order = self.env['sale.order']
        order_ids = []
        for rec in orders:
            order = rec['data']
            order_obj = False
            # if order['erp_id'] and order['erp_state'] != 'draft':

            #     self.cancel_sale_to_draft(cr, uid, order['erp_id'], context)
            #     order['erp_state'] = 'draft'

            vals = self.get_head_order_vals(order)

            if order['erp_id'] and order['erp_state'] == 'draft':
                order_obj = t_order.browse(order['erp_id'])
                order_obj.write(vals)
            else:
                vals['chanel'] = 'telesale'
                order_obj = t_order.create(vals)

            order_ids.append(order_obj.id)

            order_lines = order['lines']

            if order['erp_id'] and order['erp_state'] == 'draft':
                t_order_line = self.env['sale.order.line']
                domain = [('order_id', '=', order_obj.id)]
                line_objs = t_order_line.search(domain)
                line_objs.unlink()
            self._create_lines_from_ui(order_obj, order_lines)
            if order['action_button'] == 'confirm':
                order_obj.action_confirm()
            # MIG11 comentado, no dependo del commercial rules
            # if 'set_promotion' in order and order['set_promotion']:
            #     order_obj.apply_commercial_rules()
        return order_ids

    def _create_lines_from_ui(self, order_obj, order_lines):
        t_order_line = self.env['sale.order.line']
        for line in order_lines:
            vals = self._get_ts_line_vals(order_obj, line)
            # import pudb.remote
            # pudb.remote.set_trace(term_size=(271, 64))
            t_order_line.create(vals)

    def _get_ts_line_vals(self, order_obj, line):
        t_product = self.env['product.product']
        product_obj = t_product.browse(line['product_id'])
        product_uom_id = line.get('product_uom', False)
        product_uom_qty = line.get('qty', 0.0)
        vals = {
            'order_id': order_obj.id,
            # 'partner_id': order_obj.partner_id.id,
            'name': product_obj.display_name,
            'product_id': product_obj.id,
            'price_unit': line.get('price_unit', 0.0),
            'product_uom': product_uom_id or 1,
            'product_uom_qty': product_uom_qty,
            'tax_id': [(6, 0, line.get('tax_ids', False))],
            'discount': line.get('discount', 0.0),
        }
        return vals

    @api.model
    def confirm_order_from_ui(self, order_id):
        self.browse(order_id).action_confirm()

    @api.model
    def cancel_order_from_ui(self, order_id):
        self.browse(order_id).action_cancel()

    @api.model
    def ts_onchange_partner_id(self, partner_id):
        res = {}
        order_t = self.env['sale.order']
        partner = self.env['res.partner'].browse(partner_id)

        order = order_t.new({
                            # 'partner_id': partner_id,
                             'date_order': time.strftime("%Y-%m-%d"),
                             'pricelist_id':
                             partner.property_product_pricelist.id})
        order.onchange_partner_id()
        order.onchange_partner_shipping_id()
        res.update({
            'pricelist_id': order.pricelist_id.id,
            'partner_shipping_id': order.partner_shipping_id.id,
            'fiscal_position_id': order.fiscal_position_id.id,
            'payment_term_id': order.payment_term_id.id,
            'payment_mode_id': order.payment_mode_id.id,
        })
        return res
    
    @api.model
    def action_telesale_mail(self, order_id):
        self.env.ref('sale.email_template_edi_sale').send_mail(order_id)   
        return
        


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Because of performance options:
    standard_price = fields.Float('Intercompany Price',
                                  related='product_id.standard_price')

    @api.model
    def ts_product_id_change(self, product_id, partner_id, pricelist_id):
        res = {}
        order_t = self.env['sale.order']
        partner = self.env['res.partner'].browse(partner_id)
        if not pricelist_id:
            pricelist_id = partner.property_product_pricelist.id
        order = order_t.new({'partner_id': partner_id,
                             'date_order': time.strftime("%Y-%m-%d"),
                             'pricelist_id': pricelist_id})
        line = self.new({'order_id': order.id,
                         'product_id': product_id})
        line.product_id_change()
        line._onchange_discount()
        res.update({
            'price_unit': line.price_unit,
            'product_uom': line.product_uom.id,
            'product_uom_qty': line.product_uom_qty,
            'discount': line.discount,
            'tax_id': [x._origin.id for x in line.tax_id],
            'standard_price': line.product_id.standard_price

        })
        return res

    @api.model
    def ts_product_uom_change(self, product_id, partner_id, pricelist_id, qty):
        res = {}
        order_t = self.env['sale.order']
        partner = self.env['res.partner'].browse(partner_id)
        if not pricelist_id:
            pricelist_id = partner.property_product_pricelist.id
        order = order_t.new({'partner_id': partner_id,
                             'date_order': time.strftime("%Y-%m-%d"),
                             'pricelist_id': pricelist_id})
        prod = self.env['product.product'].browse(product_id)
        line = self.new({'order_id': order.id,
                         'product_id': product_id,
                         'product_uom': prod.uom_id.id,
                         'product_uom_qty': qty})
        line.product_uom_change()
        res.update({
            'price_unit': line.price_unit,
        })
        return res

    @api.model
    def get_last_lines_by(self, period, partner_id):
        """
        """
        cr = self._cr
        date_str = date.today()

        user = self.env['res.users'].browse(self._uid)
        company_id = user.company_id.id
        if period == "ult":
            sq = """ SELECT id
                     FROM sale_order_line sol
                     WHERE order_id in
                        (SELECT id
                         FROM sale_order WHERE
                         state in ('sale','done')
                         and company_id = %s
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
                         and so.company_id = %s
                         ORDER BY product_id desc, id desc) AS sq
                    ORDER BY id desc"""

        if period != 'ult':
            cr.execute(sq, (partner_id, date_str, company_id))
        else:
            cr.execute(sq, (company_id, partner_id))
        fetch = cr.fetchall()
        prod_ids = [x[0] for x in fetch]
        res = []
        for l in self.browse(prod_ids):
            dic = {
                'product_id': (l.product_id.id, l.product_id.name),
                'price_unit': l.product_id.list_price,
                'default_code': l.product_id.default_code
            }
            res.append(dic)
        return res
    
    @api.model
    def ts_get_sale_history(self, partner_id, pricelist_id, offset=0, limit=20):
        """
        """
        cr = self._cr

        user = self.env['res.users'].browse(self._uid)
        company_id = user.company_id.id
        sq = """ SELECT id
                    FROM sale_order_line sol
                    WHERE order_id in
                    (SELECT id
                        FROM sale_order WHERE
                        state in ('sale','done')
                        and company_id = %s
                        and partner_id = %s order by id desc)
                ORDER BY id desc LIMIT %s OFFSET %s"""

        cr.execute(sq, (company_id, partner_id, limit, offset))
        fetch = cr.fetchall()
        prod_ids = [x[0] for x in fetch]

        res = []
        for l in self.browse(prod_ids):
            # tax_ids = self.env['product.product'].\
            #     _ts_compute_taxes(l.product_id.id,
            #                       l.product_id.taxes_id,
            #                       partner_id)
            result = self.env['sale.order.line'].\
                ts_product_id_change(l.product_id.id, partner_id, pricelist_id)

            # Get price
            price = l.price_unit
            price_today = l.price_unit
            if result.get('price_unit', 0.0):
                price_today = result['price_unit']
            
            # Get taxes
            tax_ids = result.get('tax_id', [])
            dic = {
                'product_id': l.product_id.id,
                'name': l.product_id.display_name,
                'date': l.order_id.date_order,
                'qty': l.product_uom_qty,
                'price': price,
                'price_today': price_today,
                'discount': l.discount,
                'subtotal': l.price_subtotal,
                'taxes_ids': tax_ids
            }
            res.append(dic)
        
        init = offset + 1
        end = init + (limit -1)
        result_str = "%s - %s / %s" % (init, end, len(prod_ids))
        return {'history_lines': res, 'result_str': result_str}
