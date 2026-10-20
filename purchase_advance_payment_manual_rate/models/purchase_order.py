# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _compute_purchase_advance_payment(self):
        """Order in company currency paid with a foreign currency advance.

        The base method converts the advance with the system rate. If the rate
        of the payment was typed by hand, the amount in company currency of the
        payment is the right one.
        """
        super()._compute_purchase_advance_payment()
        for order in self:
            company_currency = order.company_id.currency_id
            if order.currency_id != company_currency:
                continue
            delta = self._get_manual_rate_delta_from_move_lines(order)
            delta += self._get_manual_rate_delta_from_payments(order)
            if not order.currency_id.is_zero(delta):
                order.amount_residual += delta
                if order.advance_payment_status != "not_paid":
                    has_due = order.currency_id.compare_amounts(
                        order.amount_residual, 0.0
                    )
                    order.advance_payment_status = "paid" if has_due <= 0 else "partial"

    def _get_manual_rate_delta_from_move_lines(self, order):
        """Payments with journal entry (same lines as the base method)."""
        delta = 0.0
        for line in order.payment_line_ids:
            payment = line.move_id.origin_payment_id
            if (
                not payment.use_manual_rate
                or not line.currency_id
                or line.currency_id == order.currency_id
            ):
                continue
            system_amount = line.currency_id._convert(
                line.amount_residual_currency,
                order.currency_id,
                order.company_id,
                line.date or fields.Date.today(),
            )
            delta += system_amount - line.amount_residual
        return delta

    def _get_manual_rate_delta_from_payments(self, order):
        """Payments without journal entry (same filter as the base method)."""
        delta = 0.0
        for payment in order.account_payment_ids:
            if (
                not payment.use_manual_rate
                or payment.state not in ("in_process", "paid")
                or payment.outstanding_account_id
                or payment.move_id
                or payment.invoice_ids
                or payment.currency_id == order.currency_id
            ):
                continue
            system_amount = payment.currency_id._convert(
                payment.amount,
                order.currency_id,
                order.company_id,
                payment.date or fields.Date.today(),
            )
            delta += system_amount - payment.amount / payment.manual_rate
        return delta
