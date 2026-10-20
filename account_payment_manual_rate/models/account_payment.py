# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class AccountPayment(models.Model):
    _inherit = ["account.payment", "manual.currency.rate.mixin"]
    _name = "account.payment"

    @api.depends("company_id", "currency_id", "date")
    def _compute_manual_rate_context(self):
        for payment in self:
            payment.manual_rate_company_id = payment.company_id
            payment.manual_rate_base_currency_id = payment.company_id.currency_id
            payment.manual_rate_currency_id = payment.currency_id
            payment.manual_rate_date = payment.date

    @api.model
    def _get_trigger_fields_to_synchronize(self):
        return (*super()._get_trigger_fields_to_synchronize(), "manual_rate")

    def _prepare_move_lines_per_type(self, write_off_line_vals=None, force_balance=None):
        res = super()._prepare_move_lines_per_type(
            write_off_line_vals=write_off_line_vals, force_balance=force_balance
        )
        if not self._manual_rate_applies():
            return res
        if force_balance is not None and not write_off_line_vals:
            # The caller already set the balance of the payment.
            return res
        liquidity_lines = res["liquidity_lines"]
        counterpart_lines = res["counterpart_lines"]
        if len(liquidity_lines) != 1 or len(counterpart_lines) != 1:
            return res
        withholding_lines = res.get("withholding_lines", [])
        withholding_amount_currency = sum(x["amount_currency"] for x in withholding_lines)
        withholding_balance = sum(x["balance"] for x in withholding_lines)
        write_off_balance = sum(x["balance"] for x in res.get("write_off_lines", []))

        # The liquidity line carries the whole payment amount minus withholdings.
        payment_amount_currency = (
            liquidity_lines[0]["amount_currency"] + withholding_amount_currency
        )
        liquidity_balance = (
            self._manual_rate_convert(payment_amount_currency) - withholding_balance
        )
        liquidity_lines[0]["balance"] = liquidity_balance
        counterpart_lines[0]["balance"] = (
            -liquidity_balance - write_off_balance - withholding_balance
        )
        return res
