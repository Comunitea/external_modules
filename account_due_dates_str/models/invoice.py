# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api
from odoo.tools import formatLang, format_date
import math


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    def get_expiration_dates_list(self, padding, signed):
        sign = 1
        if signed and 'refund' in self.type:
            sign = -1
        self.ensure_one()
        expiration_dates = []
        if self.move_id:
            move_lines = self.env["account.move.line"].\
                search([('move_id', '=', self.move_id.id),
                        ('account_id.internal_type', 'in',
                            ['payable', 'receivable']),
                        ('date_maturity', "!=", False)],
                       order="date_maturity asc")
            for line in move_lines:
                currency = self.currency_id
                if self.type in ('out_invoice', 'in_refund'):
                    quantity = formatLang(
                        self.env, sign * line.debit, currency_obj=currency)
                else:
                    quantity = formatLang(self.env, sign * line.credit)
                expiration_dates.append('{} {}> {}'.format(
                    format_date(self.env, line.date_maturity), '-' * padding,
                    quantity))
        return expiration_dates

    def get_expiration_dates_tuples(self, padding=1, signed=False):
        self.ensure_one()
        expiration_date_list = []
        expiration_dates = self.get_expiration_dates_list(padding, signed)
        curr_pos = 0
        for i in range(math.ceil(len(expiration_dates) / 2)):
            curr_expiration = expiration_dates[curr_pos]
            if curr_pos + 1 <= len(expiration_dates) - 1:
                curr_expiration_1 = expiration_dates[curr_pos + 1]
            else:
                curr_expiration_1 = None
            expiration_date_list.append(
                (curr_expiration, curr_expiration_1))
            curr_pos += 2
        return expiration_date_list



    @api.multi
    def _compute_expiration_dates_str(self):
        """returns all due dates related to invoice in string"""
        for invoice in self:
            expiration_dates = invoice.get_expiration_dates_list(1, False)
            invoice.expiration_dates_str = '\n'.join(expiration_dates)

    expiration_dates_str = fields.Text('Expiration dates', readonly=True,
                                       compute='_compute_expiration_dates_str')
