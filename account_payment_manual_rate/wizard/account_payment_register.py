# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = ["account.payment.register", "manual.currency.rate.mixin"]
    _name = "account.payment.register"

    @api.depends("company_id", "currency_id", "source_currency_id", "payment_date")
    def _compute_manual_rate_context(self):
        """Pick the pair of currencies the rate refers to.

        * Payment in a foreign currency, paying items in that same currency or
          in the company one: rate of the payment currency (it is the rate of
          the journal entry of the payment).
        * Payment in the company currency paying items in a foreign currency:
          rate of the items currency, forced in the reconciliation so the
          items are paid at that rate without exchange differences.
        * Otherwise there is no sensible rate.
        """
        for wizard in self:
            company_currency = wizard.company_id.currency_id
            currency = wizard.currency_id
            source = wizard.source_currency_id
            if currency and currency != company_currency:
                if source and source not in (currency, company_currency):
                    currency = False
            elif source and source != company_currency:
                currency = source
            else:
                currency = False
            wizard.manual_rate_company_id = wizard.company_id
            wizard.manual_rate_base_currency_id = company_currency
            wizard.manual_rate_currency_id = currency
            wizard.manual_rate_date = wizard.payment_date

    @api.depends("can_edit_wizard", "can_group_payments", "group_payment")
    def _compute_manual_rate_available(self):
        super()._compute_manual_rate_available()
        for wizard in self:
            # The rate only makes sense when the amount and currency are editable.
            wizard.manual_rate_available = (
                wizard.manual_rate_available
                and wizard.can_edit_wizard
                and (not wizard.can_group_payments or wizard.group_payment)
            )

    def _manual_rate_mode(self):
        """Return 'payment', 'reconcile' or False (no manual rate applied)."""
        self.ensure_one()
        if not self._manual_rate_applies():
            return False
        if self.manual_rate_currency_id == self.currency_id:
            return "payment"
        return "reconcile"

    # The amounts to pay are converted with the manual rate
    @api.depends("manual_rate")
    def _compute_amount(self):
        return super()._compute_amount()

    @api.depends("manual_rate")
    def _compute_payment_difference(self):
        return super()._compute_payment_difference()

    @api.depends("manual_rate")
    def _compute_installments_mode(self):
        return super()._compute_installments_mode()

    def _convert_to_wizard_currency(self, installments):
        self.ensure_one()
        mode = self._manual_rate_mode()
        lines = self.env["account.move.line"].union(
            *[installment["line"] for installment in installments]
        )
        if not mode or not lines:
            return super()._convert_to_wizard_currency(installments)
        company_currency = self.company_currency_id
        if mode == "reconcile" and lines.currency_id == self.manual_rate_currency_id:
            total = sum(x["amount_residual_currency"] for x in installments)
            return self.currency_id.round(total / self.manual_rate)
        if (
            mode == "payment"
            and lines.currency_id == company_currency
            and self.currency_id != company_currency
        ):
            total = sum(x["amount_residual"] for x in installments)
            return self.currency_id.round(total * self.manual_rate)
        return super()._convert_to_wizard_currency(installments)

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        mode = self._manual_rate_mode()
        if not mode:
            return payment_vals
        # The user rate prevails over the one of the reconciled journal items.
        payment_vals.pop("force_balance", None)
        if mode == "payment":
            payment_vals.update(self._manual_rate_vals())
            if not self.early_payment_discount_mode:
                for write_off_vals in payment_vals["write_off_line_vals"]:
                    write_off_vals["balance"] = self._manual_rate_convert(
                        write_off_vals["amount_currency"]
                    )
        return payment_vals

    def _init_payments(self, to_process, edit_mode=False):
        # Don't let Odoo adjust the balance to the one of the source items.
        if edit_mode and self._manual_rate_mode():
            edit_mode = False
        return super()._init_payments(to_process, edit_mode=edit_mode)

    def _reconcile_payments(self, to_process, edit_mode=False):
        if edit_mode and self._manual_rate_mode() == "reconcile":
            # Reconcile the items at the manual rate instead of the system one
            for vals in to_process:
                vals["rate"] = self.manual_rate
        return super()._reconcile_payments(to_process, edit_mode=edit_mode)
