# Copyright 2018 Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models, fields, _


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    invoice_policy = fields.Selection([
        ('product', 'Inherit from product'),
        ('order', 'Ordered quantities'),
        ('delivery', 'Delivered quantities')], string='Invoicing Policy',
        help='Ordered Quantity: Invoice quantities ordered by the customer.\n'
             'Delivered Quantity: Invoice quantities delivered to the customer.',
        default='product')

    @api.depends('qty_invoiced', 'qty_delivered', 'product_uom_qty', 'order_id.state', 'invoice_policy')
    def _get_to_invoice_qty(self):
        """
        Compute the quantity to invoice. If the invoice policy is order, the quantity to invoice is
        calculated from the ordered quantity. Otherwise, the quantity delivered is used.
        """
        super()._get_to_invoice_qty()
        for line in self.filtered(lambda x: x.invoice_policy != 'product'):
            if line.order_id.state in ['sale', 'done']:
                if line.invoice_policy == 'order':
                    line.qty_to_invoice = line.product_uom_qty - line.qty_invoiced
                else:
                    line.qty_to_invoice = line.qty_delivered - line.qty_invoiced
            else:
                line.qty_to_invoice = 0