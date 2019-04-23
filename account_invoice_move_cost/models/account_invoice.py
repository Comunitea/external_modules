# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.tools import float_compare


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        """ Validated invoice generate cross invoice base on company rules """
        res = super(AccountInvoice, self).action_invoice_open()
        for invoice in self:
            if invoice.type == 'in_invoice':
                for line in invoice.invoice_line_ids:
                    pur_line = line.purchase_line_id
                    if pur_line and line.price_subtotal > 0 and \
                            line.product_id.cost_method == 'fifo':
                        inv_price = line._get_stock_move_price_unit()
                        pur_price = pur_line._get_stock_move_price_unit()
                        #if inv_price != pur_price:
                        for move in pur_line.move_ids:
                            if move._is_in() and move.remaining_qty > 0:
                                remaining_value = move.remaining_qty * \
                                                  inv_price
                                move.write({
                                    'remaining_value': remaining_value})
        return res


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    def _get_stock_move_price_unit(self):
        self.ensure_one()
        line = self[0]
        invoice = line.invoice_id
        price_unit = line.price_unit
        if line.invoice_line_tax_ids:
            price_unit = line.invoice_line_tax_ids.with_context(round=False).compute_all(
                price_unit, currency=line.invoice_id.currency_id,
                quantity=1.0, product=line.product_id,
                partner=line.invoice_id.partner_id
            )['total_excluded']
        if line.uom_id.id != line.product_id.uom_id.id:
            price_unit *= line.uom_id.factor / line.product_id.uom_id.factor
        if invoice.currency_id != invoice.company_id.currency_id:
            price_unit = invoice.currency_id.with_context(date=invoice.date).compute(price_unit, invoice.company_id.currency_id, round=False)
        if line.discount:
            return price_unit * (1 - line.discount / 100)
        return price_unit