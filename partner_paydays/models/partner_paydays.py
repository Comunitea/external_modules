# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta
from odoo import models, fields, api, _, exceptions


class ResPartner(models.Model):

    _inherit = "res.partner"

    @api.one
    @api.constrains("payment_days")
    def _check_payment_days(self):
        if not self.payment_days:
            return
        try:
            payment_days = self.env[
                "account.payment.term"
            ]._decode_payment_days(self.payment_days)
            error = any(day <= 0 or day > 31 for day in payment_days)
        except:
            error = True
        if error:
            raise exceptions.UserError(
                _("Payment days field format is not valid.")
            )

    payment_days = fields.Char(
        "Payment days",
        size=11,
        help="If a company has more than one payment days in a month "
        "you should fill them in this field and set 'Day of the "
        "Month' field in line to zero. For example, if a company "
        "pays the 5th and 20th days of the month you should write "
        "'5-20' here.",
    )
    pays_during_holidays = fields.Boolean(
        "Pays During Holidays",
        help="Indicates whether the partner pays during holidays. "
        "If it doesn''t, it will be taken into account when "
        "calculating due dates.",
        default=True,
    )
    holiday_ids = fields.One2many(
        "res.partner.holidays", "partner_id", "Holidays"
    )


class ResPartnerHolidays(models.Model):

    _name = "res.partner.holidays"
    _order = "start DESC"

    partner_id = fields.Many2one(
        "res.partner", "Partner", required=True, ondelete="cascade"
    )
    start = fields.Date("Start", required=True)
    end = fields.Date("End", required=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.start, record.end)))
        return result


class AccountPaymentTerm(models.Model):

    _inherit = "account.payment.term"

    reference_date = fields.Selection(
        [("value_date", "Fecha valor"), ("invoice_date", "Fecha Factura")],
        string="Fecha de referencia",
        default="invoice_date",
    )

    @api.model
    def _decode_payment_days(self, days_char):
        # Admit space, dash and comma as separators
        days_char = days_char.replace(" ", "-").replace(",", "-")
        days_char = [x.strip() for x in days_char.split("-") if x]
        days = [int(x) for x in days_char]
        days.sort()
        return days

    @api.model
    def days_in_month(self, date_in):
        if date_in.month == 12:
            date_in = date_in.replace(day=31)
        else:
            date_in = date_in.replace(month=date_in.month + 1, day=1) - timedelta(days=1)
        return date_in.day

    @api.model
    def next_day(self, date_in, day):
        if date_in.day == day:
            return date_in
        if day < 1:
            day = 1
        if day > self.days_in_month(date_in):
            day = self.days_in_month(date_in)
        while True:

            if date_in.day == day:
                return date_in
            date_in += timedelta(days=1)

    @api.model
    def _after_holidays(self, partner, date_in, days):
        for holidays in partner.holiday_ids:
            start = datetime.strptime(
                holidays.start.strftime(
                    date_in.strftime("%Y") + "-%m-%d"
                ),
                "%Y-%m-%d",
            )
            end = datetime.strptime(
                holidays.end.strftime(
                    date_in.strftime("%Y") + "-%m-%d"
                ),
                "%Y-%m-%d",
            )
            if date_in >= start and date_in <= end:
                date_in = end + timedelta(days=1)
            found = False
            for day in days:
                if date_in.day <= day:
                    date_in = self.next_day(date_in, day)
                    found = True
                    break
            if days and not found:
                date_in = self.next_day(date_in, days[0])
        return date_in

    def compute(self, value, date_ref=False):
        # TODO REVISAR SANTI / OMAR
        if self._context.get("invoice_id", False):
            invoice = self.env["account.invoice"].browse(
                self._context["invoice_id"]
            )

            if (
                invoice.value_date
                and invoice.payment_term_id.reference_date == "value_date"
            ):
                date_ref = invoice.value_date
            elif invoice.payment_ref_date:
                date_ref = invoice.payment_ref_date

        result = super(AccountPaymentTerm, self).compute(value, date_ref)

        if not self.env.context.get("partner_id"):
            return result
        partner = self.env["res.partner"].browse(self.env.context["partner_id"])
        if not partner.payment_days:
            return result

        days = self._decode_payment_days(partner.payment_days)

        new_result = []
        for line in result[0]:
            new_date = False
            line_date = datetime.strptime(line[0], "%Y-%m-%d")

            for day in days:
                if line_date.day <= day:
                    new_date = self.next_day(line_date, day)
                    break

            if days:
                if not new_date:
                    day = days[0]
                    line_date = self.next_day(line_date, day)
                else:
                    line_date = new_date

            if not partner.pays_during_holidays:
                line_date = self._after_holidays(partner, line_date, days)
            new_result.append((line_date.date(), line[1]))
        return [new_result]
