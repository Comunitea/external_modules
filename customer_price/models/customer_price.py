# © 2019 Santi Argueso <santi@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
import odoo.addons.decimal_precision as dp
import time


class CustomerPrice(models.Model):
    _name = "customer.price"

    product_tmpl_id = fields.Many2one('product.template', 'Template',
                                      index=1)
    product_id = fields.Many2one('product.product', 'Product', index=1)
    partner_id = fields.Many2one('res.partner', 'Customer', required=True,
                                 index=1)
    min_qty = fields.Float('Min Quantity', default=0.0, required=True)
    price = fields.Float(
        'Price', default=0.0, digits=dp.get_precision('Product Price'),
        required=True, help="The price to purchase a product")
    date_start = fields.Date('Start Date', index=1,
                             help="Start date for this customer price")
    date_end = fields.Date('End Date', index=1,
                           help="End date for this customer price")
    company_id = fields.\
        Many2one('res.company', 'Company',
                 default=lambda self: self.env.user.company_id.id, index=1)

    @api.model
    def get_customer_price(self, partner_id, product, qty, date=False):
        today = date or time.strftime('%Y-%m-%d')
        if isinstance(partner_id, (int,)):
            partner = partner_id
        else:
            partner = partner_id.id
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
        if customer_prices:
            return customer_prices.price
        return False
