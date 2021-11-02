# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _, fields
from openerp.exceptions import except_orm


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_id = fields.Many2one(index=True, auto_join=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_tmpl_id = fields.Many2one(index=True, auto_join=True)

    @api.model
    def fetch_product_data(self, field_list, domain):
        """
        Get the products as fast as posible, with only id in many to one
        """
        products = self.search(domain)
        res = products.read(field_list, load='_classic_write')
        return res

    @api.model
    def get_product_info(self, product_id, partner_id):
        """ Return data of widget productInfo """

        res = {
            'stock': 0.0,
            'last_date': "-",
            'last_qty': 0.0,
            'last_price': 0.0,
        }
        t_sol = self.env['sale.order.line']
        if not product_id or not partner_id:
            raise except_orm(_('Error!'), _("Product_id or partrner_id \
                                            must be defined"))
        product_obj = self.browse(product_id)
        res['stock'] = product_obj.virtual_available
        domain = [('product_id', '=', product_id),
                  ('order_id.partner_id', '=', partner_id),
                  ('state', 'in', ['sale', 'done']),
                  ]
        line_obj = t_sol.search(domain, limit=1, order="id desc")
        if line_obj:  # Last sale info
            res['last_date'] = line_obj.order_id.date_order
            res['last_qty'] = line_obj.product_uom_qty
            res['last_price'] = line_obj.price_unit
        return res

    @api.model
    def _get_line_discount(self, line):
        return line.discount

    @api.model
    def get_history_product_info(self, product_id, partner_id):
        """ Return data of widget productInfo History """
        res = []
        t_sol = self.env['sale.order.line']
        if not product_id or not partner_id:
            raise except_orm(_('Error!'), _("Product_id or partrner_id \
                                            must be defined"))
        domain = [('product_id', '=', product_id),
                  ('order_id.partner_id', '=', partner_id),
                  ('state', 'in', ['sale', 'done']),
                  ]
        lines_objs = t_sol.search(domain, order="id desc")
        for line in lines_objs:
            vals = {
                'date': line.order_id.date_order,
                'qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'discount': self._get_line_discount(line)
            }
            res.append(vals)
        return res

    @api.model
    def _get_stock_field(self):
        return 'qty_available'

    @api.model
    def _ts_compute_taxes(self, product_id, tax_ids, partner_id):
        res = tax_ids
        if partner_id and tax_ids:
            partner = self.env['res.partner'].browse(partner_id)
            product = self.env['product.product'].browse(product_id)
            fpos = partner.property_account_position_id
            if fpos:
                taxes = self.env['account.tax'].browse(tax_ids)
                res = fpos.map_tax(taxes, product, partner).ids
        return res

    @api.model
    def ts_search_products(self, product_name, product_barcode, partner_id,
                           pricelist_id, offset=0):
        res = []
        # import ipdb; ipdb.set_trace()
        domain = ['|', ('name', 'ilike', product_name), ('default_code', 'ilike', product_name)]
        if product_barcode:
            domain2 = ('barcode', 'ilike', product_barcode)
            if product_name:
                domain.append(domain2)
            else:  # Only search by barcode
                domain = [domain2]
        stock_field = self._get_stock_field()
        fields = ['id', 'name', 'default_code', 'barcode', stock_field, 'price',
                  'taxes_id']
        ctx = self._context.copy()
        ctx.update(pricelist=pricelist_id, partner=partner_id)
        read = self.with_context(ctx).search_read(domain, fields, limit=100,
                                                  offset=offset)

        for dic in read:
            # tax_ids = self._ts_compute_taxes(dic['id'],
            #                                  dic.get('taxes_id', []),
            #                                  partner_id)
            result = self.env['sale.order.line'].\
                ts_product_id_change(dic['id'], partner_id, pricelist_id)

            # Get the correct price and discount
            price = dic.get('price', 0.0)
            discount = dic.get('discount', 0.0)
            if result.get('price_unit', 0.0):
                price = result['price_unit']
            if result.get('discount', 0.0):
                discount = result['discount']

            # Get taxes
            tax_ids = result.get('tax_id', [])
            formated = {
                'id': dic['id'],
                'display_name': "[" + dic.get('default_code', '') + "] " + dic.get('name', 0.0),
                'barcode': dic.get('barcode', 0.0),
                'stock': dic.get(stock_field, 0.0),
                'price': price,
                'discount': discount,
                # Esto tendría que estar abstraidoy en jim_telesale
                # meter el chained discount. Aun así no va a fallar
                'chained_discount': str(discount),
                'qty': 0.0,
                'tax_ids': tax_ids,
            }
            res.append(formated)

        init = offset + 1
        end = init + 99
        total = len(self.search(domain))
        show_next = True
        if total < end:
            end = total
            show_next = False
        result_str = "%s - %s / %s" % (init, end, total)
        result = {
            'result_str': result_str,
            'products': res,
            'show_next': show_next,
            'show_prev': (init != 1)
        }
        return result

    @api.model
    def _get_onchange_vals(self, product, partner_id, pricelist_id):
        res = {
            'price': 0.0,
            'tax_ids': []
        }
        if partner_id and product:
            values = self.env['sale.order.line'].\
                ts_product_id_change(product.id, partner_id, pricelist_id)
            res.update({
                'price': values.get('price_unit', 0.0),
                'tax_ids': values.get('tax_id', [])
            })
        return res

    @api.model
    def _get_product_stock(self, product):
        return product and product.qty_available or 0
