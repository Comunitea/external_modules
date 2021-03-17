# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    def action_invoice_open(self):
        res = super().action_invoice_open()
        for invoice in self:
            if invoice.type == 'in_invoice':
                for line in invoice.invoice_line_ids:
                    pur_line = line.purchase_line_id
                    if pur_line and line.price_subtotal > 0:
                        inv_price = line._get_stock_move_price_unit()
                        for move in pur_line.move_ids.filtered(lambda a: a.state=='done'):
                            if move._is_in() and move.remaining_qty > 0:
                                remaining_value = move.remaining_qty * \
                                                  inv_price
                                move.write({
                                    'remaining_value': remaining_value})
                        if  line.product_id.cost_method == 'average':
                            d = {}

                            for move in pur_line.move_ids.filtered(lambda a: a.state=='done'):

                                if inv_price != move.price_unit:
                                    product = move.product_id
                                    d.setdefault(product, [])
                                    d[product].append(
                                        (move,
                                        inv_price - move.price_unit)
                                    )
                            for product, vals_list in d.items():
                                self._product_price_update(product, vals_list)
                                for move, price_diff in vals_list:
                                    move.price_unit += price_diff
                                    move.value = move.product_uom_qty * move.price_unit

        return res



    def _product_price_update(self, product, vals_list):
        """Method that mimicks stock.move's product_price_update_before_done
        method behaviour, but taking into account that calculations are made
        on an already done moves, and prices sources are given as parameters.
        """
        moves_total_qty = 0
        moves_total_diff_price = 0
        for move, price_diff in vals_list:
            moves_total_qty += move.product_qty
            moves_total_diff_price += move.product_qty * price_diff
        prev_qty_available = product.qty_available - moves_total_qty
        if prev_qty_available <= 0:
            prev_qty_available = 0
        total_available = prev_qty_available + moves_total_qty
        new_std_price = (
            (total_available * product.standard_price +
             moves_total_diff_price) / total_available
        )
        # Write the standard price, as SUPERUSER_ID, because a
        # warehouse manager may not have the right to write on products
        product.sudo().write({'standard_price': new_std_price})



class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    def _get_stock_move_price_unit(self):
        self.ensure_one()
        invoice = self.invoice_id
        price_unit = self.price_unit
        if self.invoice_line_tax_ids:
            price_unit = self.invoice_line_tax_ids.with_context(
                round=False).compute_all(
                    price_unit, currency=self.invoice_id.currency_id,
                    quantity=1.0, product=self.product_id,
                    partner=self.invoice_id.partner_id
            )['total_excluded']
        if self.uom_id.id != self.product_id.uom_id.id:
            price_unit *= self.uom_id.factor / self.product_id.uom_id.factor
        if invoice.currency_id != invoice.company_id.currency_id:
            price_unit = invoice.currency_id.with_context(
                date=invoice.date).compute(
                    price_unit, invoice.company_id.currency_id, round=False)
        if self.discount:
            return price_unit * (1 - self.discount / 100)
        return price_unit
