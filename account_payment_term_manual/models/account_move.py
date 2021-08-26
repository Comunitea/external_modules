# © 2017 Comunitea Servicios Tecnológicos S.L.
#        (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, _, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    manual_term = fields.Boolean("Manual Payment Term ")

    def compute(self, value, date_ref=False, currency=None):
        self.ensure_one()
        result = []
        if not self.env.context.get('manual_term'):
            result = super().compute(value, date_ref=date_ref,
                                     currency=currency)
        else:
            date_ref = date_ref or fields.Date.context_today(self)
            sign = value < 0 and -1 or 1
            value = abs(value)
            amount = value
            if not currency and self.env.context.get('currency_id'):
                currency = self.env['res.currency'].\
                    browse(self.env.context['currency_id'])
            elif not currency:
                currency = self.env.company.currency_id
            ipt = self._context.get('initial_payment_type')
            ipa = self._context.get('initial_payment_amount')
            nop = self._context.get('number_of_payments')
            if nop <= 0:
                raise UserError(_('Wrong number of payments. Please correct '
                                  'it in Invoice'))
            if ipt == 'fixed':
                first_amt = currency.round(ipa)
                result.append((date_ref, sign * first_amt))
            else:
                first_amt = currency.round(value * (ipa / 100.0))
                result.append((date_ref, sign * first_amt))
            res_amt = amount - first_amt
            if res_amt:
                date_ref = fields.Date.from_string(date_ref)
                date_ref += relativedelta(days=30)
                if nop < 2:
                    raise UserError(
                        _('Wrong number of payments. Please correct '
                          'it in Invoice'))
                line_amt = currency.round(res_amt / (nop-1))
                for x in range(1, nop-1):
                    result.append((fields.Date.to_string(date_ref),
                                   sign * line_amt))
                    res_amt -= line_amt
                    date_ref += relativedelta(days=30)
            if res_amt:
                result.append((fields.Date.to_string(date_ref),
                               sign * res_amt))
        return result


class AccountMove(models.Model):
    _inherit = "account.move"

    manual_term_check = fields.\
        Boolean(related='invoice_payment_term_id.manual_term')
    initial_payment_type = fields.Selection([
            ('percent', 'Percent'),
            ('fixed', 'Fixed Amount')],
        string='Initial Payment Type', required=False, default='percent',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Select here the kind of valuation related to first payment term "
             "line.")
    initial_payment_amount = fields.Monetary(
        string='Initial payment (fixed or %)',
        readonly=True, states={'draft': [('readonly', False)]})
    number_of_payments = fields.\
        Integer(default=2, readonly=True,
                states={'draft': [('readonly', False)]},
                help="Number of payments included initial.")

    @api.onchange('initial_payment_type', 'initial_payment_amount',
                  'number_of_payments', 'invoice_payment_term_id',
                  'line_ids', 'invoice_date_due', 'invoice_cash_rounding_id',
                  'invoice_vendor_bill_id')
    def _onchange_recompute_dynamic_lines(self):
        if self.invoice_payment_term_id and self.invoice_payment_term_id.\
                manual_term:
            super(AccountMove,
                  self.with_context(manual_term=True,
                                    initial_payment_type=self.
                                    initial_payment_type,
                                    initial_payment_amount=self.
                                    initial_payment_amount,
                                    number_of_payments=self.
                                    number_of_payments)).\
                    _onchange_recompute_dynamic_lines()
        else:
            super()._onchange_recompute_dynamic_lines()
