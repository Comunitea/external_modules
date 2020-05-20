# © 2019 Santi Argueso <santi@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
import time


class CustomerPrice(models.Model):
    _name = "customer.price"
    _description = 'customer price'

    product_tmpl_id = fields.Many2one('product.template', 'Template')
    product_id = fields.Many2one('product.product', 'Product', index=1)
    partner_id = fields.Many2one('res.partner', 'Customer', required=True)
    min_qty = fields.Float('Min Quantity', default=0.0, required=True)
    price = fields.Float(
        'Price', default=0.0, digits=dp.get_precision('Product Price'),
        required=True, help="The price to purchase a product")
    date_start = fields.Date('Start Date',
                             help="Start date for this customer price")
    date_end = fields.Date('End Date', help="End date for this customer price")
    company_id = fields.\
        Many2one('res.company', 'Company',
                 default=lambda self: self.env.user.company_id.id, index=1)

    @api.model
    def get_customer_price_rec(self, partner_id, product, qty, date=False):
        today = date or time.strftime('%Y-%m-%d')
        if isinstance(partner_id, (int,)):
            partner = self.env['res.partner'].browse(partner_id)[
                0].commercial_partner_id.id
        else:
            partner = partner_id.commercial_partner_id.id
        domain = [('partner_id', '=', partner),
                  ('product_id', '=', product.id),
                  ('min_qty', '<=', qty),
                  '|',
                  ('date_start', '=', False),
                  ('date_start', '<=', today),
                  '|',
                  ('date_end', '=', False),
                  ('date_end', '>=', today)]
        customer_prices = self.env['customer.price'].\
            search(domain, limit=1, order='min_qty desc')
        # Search for specific prices in templates
        if not customer_prices:
            domain = [
                ('partner_id', '=', partner),
                ('product_tmpl_id', '=', product.product_tmpl_id.id),
                ('min_qty', '<=', qty),
                '|',
                ('date_start', '=', False),
                ('date_start', '<=', today),
                '|',
                ('date_end', '=', False),
                ('date_end', '>=', today),
            ]
            customer_prices = self.env['customer.price'].\
                search(domain, limit=1, order='min_qty desc')
        print(customer_prices)
        return customer_prices

    @api.model
    def get_customer_price(self, partner_id, product, qty, date=False):
        customer_prices = self.sudo().get_customer_price_rec(
            partner_id, product, qty, date)
        if customer_prices:
            print(customer_prices.price)
            return customer_prices.price
        return False
