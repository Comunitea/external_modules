# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class AccountVoucherWizardPurchase(models.TransientModel):
    _inherit = ["account.voucher.wizard.purchase", "manual.currency.rate.mixin"]
    _name = "account.voucher.wizard.purchase"

    @api.depends("order_id.company_id", "journal_currency_id", "currency_id", "date")
    def _compute_manual_rate_context(self):
        """The rate converts the journal currency into the order currency.

        It is only offered when one of them is the company currency, as the
        other one is then the one that can be converted with it.
        """
        for wizard in self:
            company = wizard.order_id.company_id or wizard.env.company
            base = wizard.journal_currency_id
            currency = wizard.currency_id
            if company.currency_id not in (base, currency):
                base = currency = False
            wizard.manual_rate_company_id = company
            wizard.manual_rate_base_currency_id = base
            wizard.manual_rate_currency_id = currency
            wizard.manual_rate_date = wizard.date

    @api.depends("manual_rate")
    def _compute_currency_amount(self):
        super()._compute_currency_amount()
        for wizard in self:
            if wizard._manual_rate_applies():
                wizard.currency_amount = wizard.currency_id.round(
                    wizard.amount_advance * wizard.manual_rate
                )

    def _prepare_payment_vals(self, purchase):
        vals = super()._prepare_payment_vals(purchase)
        if not self._manual_rate_applies():
            return vals
        company_currency = self.manual_rate_company_id.currency_id
        if self.journal_currency_id == company_currency:
            # Pay the order currency amount, the journal entry gets the exact
            # amount of the journal in company currency (the rate is stored in
            # the payment to keep it if the draft payment is modified).
            vals.update(
                currency_id=self.currency_id.id,
                amount=self.currency_amount,
                manual_rate=self.manual_rate,
                force_balance=self.amount_advance,
            )
        else:
            # Payment in a foreign currency for an order in company currency
            vals.update(
                manual_inverse_rate=self.manual_rate,
                manual_rate=1.0 / self.manual_rate,
            )
        return vals
