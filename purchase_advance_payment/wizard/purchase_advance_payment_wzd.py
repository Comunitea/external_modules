# Copyright 2019 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, exceptions, _


class AccountVoucherWizard(models.TransientModel):

    _name = "account.purchase.voucher.wizard"

    @api.multi
    @api.depends('journal_id')
    def _get_journal_currency(self):
        for wzd in self:
            wzd.journal_currency_id = wzd.journal_id.currency_id.id or \
                self.env.user.company_id.currency_id.id

    journal_id = fields.Many2one('account.journal', 'Journal', required=True,
                                 domain=[('type', 'in', ('bank', 'cash'))])
    journal_currency_id = fields.Many2one("res.currency", "Journal Currency",
                                          readonly=True,
                                          compute="_get_journal_currency")
    amount_total = fields.Monetary('Amount total', readonly=True)
    amount_advance = fields.Monetary('Amount advanced', required=True)
    date = fields.Date("Date", required=True,
                       default=fields.Date.context_today)
    exchange_rate = fields.Float("Exchange rate", digits=(16, 6), default=1.0,
                                 required=True)
    currency_id = fields.Many2one("res.currency", "Currency", readonly=True)
    currency_amount = fields.Monetary("Curr. amount", readonly=True,
                                      currency_field="journal_currency_id")
    payment_ref = fields.Char("Ref.")
    due_date = fields.Date("Due date", help="If this date is set, will be "
                                            "written on bank entry")

    @api.constrains('amount_advance')
    def check_amount(self):
        if self.amount_advance <= 0:
            raise exceptions.ValidationError(_("Amount of advance must be "
                                               "positive."))
        if self.env.context.get('active_id', False):
            order = self.env["purchase.order"].\
                browse(self.env.context['active_id'])
            if self.amount_advance > order.amount_resisual:
                raise exceptions.ValidationError(_("Amount of advance is "
                                                   "greater than residual "
                                                   "amount on purchase"))

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        purchase_ids = self.env.context.get('active_ids', [])
        if not purchase_ids:
            return res
        purchase_id = purchase_ids[0]

        purchase = self.env['purchase.order'].browse(purchase_id)

        if 'amount_total' in fields:
            res.update({'amount_total': purchase.amount_resisual,
                        'currency_id': purchase.currency_id.id})

        return res

    @api.onchange('journal_id', 'date', 'amount_advance')
    def onchange_date(self):
        if self.currency_id:
            self.exchange_rate = 1.0 / \
                (self.env["res.currency"].with_context(date=self.date).
                 _get_conversion_rate(self.currency_id,
                                      self.journal_currency_id)
                 or 1.0)
        else:
            self.exchange_rate = 1.0
        self.currency_amount = self.amount_advance * (1.0 / self.exchange_rate)

    @api.multi
    def make_advance_payment(self):
        """Create customer paylines and validates the payment"""
        self.ensure_one()
        payment_obj = self.env['account.payment']
        purchase_obj = self.env['purchase.order']

        purchase_ids = self.env.context.get('active_ids', [])
        if purchase_ids:
            purchase_id = purchase_ids[0]
            purchase = purchase_obj.browse(purchase_id)

            partner_id = purchase.partner_id.commercial_partner_id.id
            company = purchase.company_id

            payment_res = {'payment_type': 'outbound',
                           'partner_id': partner_id,
                           'partner_type': 'supplier',
                           'journal_id': self.journal_id.id,
                           'company_id': company.id,
                           'currency_id': purchase.currency_id.id,
                           'payment_date': self.date,
                           'amount': self.amount_advance,
                           'purchase_id': purchase.id,
                           'name': _("Advance Payment") + " - " +
                           purchase.name,
                           'communication': self.payment_ref or purchase.name,
                           'payment_reference': self.payment_ref or
                           purchase.name,
                           'payment_method_id': self.env.
                           ref('account.account_payment_method_manual_out').id
                           }
            payment = payment_obj.create(payment_res)
            payment.post()
            payment.refresh()

            for line in payment.move_line_ids:
                if line.credit and self.due_date:
                    line.date_maturity = self.due_date

        return {
            'type': 'ir.actions.act_window_close',
        }
