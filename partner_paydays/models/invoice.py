# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    value_date = fields.Date(
        string="Fecha valor",
        states={"draft": [("readonly", False)]},
        index=True,
        copy=False,
    )
    payment_ref_date = fields.Date(
        string="Fecha referencia pagos",
        states={"draft": [("readonly", False)]},
        index=True,
        copy=False,
    )

    @api.onchange("payment_term_id", "date_invoice", "value_date")
    def _onchange_payment_term_date_invoice(self):
        if (
            self.value_date
            and self.payment_term_id.reference_date == "value_date"
        ):
            date_reference = self.value_date
        else:
            date_reference = self.payment_ref_date or self.date_invoice

        if not date_reference:
            date_reference = fields.Date.context_today(self)

        if not self.payment_term_id:
            # When no payment term defined
            self.date_due = self.date_due or self.date_invoice
        else:
            pterm = self.payment_term_id
            pterm_list = pterm.with_context(
                currency_id=self.company_id.currency_id.id,
                partner_id=self.partner_id.commercial_partner_id.id,
                invoice = self,
            ).compute(value=1, date_ref=date_reference)[0]
            self.date_due = max(line[0] for line in pterm_list)

    @api.multi
    def action_move_create(self):
        for inv in self:
            ctx = dict(
                self._context,
                invoice=inv,
                partner_id=inv.partner_id.commercial_partner_id.id,
            )
            super(AccountInvoice, inv.with_context(ctx)).action_move_create()
        return True
