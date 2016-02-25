# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 NaN Projectes de Programari Lliure, S.L.
#                       http://www.NaN-tic.com
#    Copyright (C) 2013 Pexego Sistemas Informáticos S.L.
#                       http://www.pexego.es
#    Copyright (C) 2016 Comunitea Servicios Tecnológicos S.L.
#                       http://www.comunitea.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta
from openerp import models, fields, api, _, exceptions


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.one
    @api.constrains('payment_days')
    def _check_payment_days(self):
        if not self.payment_days:
            return
        try:
            payment_days = self.env['account.payment.term'].\
                _decode_payment_days(self.payment_days)
            error = any(day <= 0 or day > 31 for day in payment_days)
        except:
            error = True
        if error:
            raise exceptions.Warning(
                _('Payment days field format is not valid.'))

    payment_days = fields.\
        Char('Payment days', size=11,
             help="If a company has more than one payment days in a month "
                  "you should fill them in this field and set 'Day of the "
                  "Month' field in line to zero. For example, if a company "
                  "pays the 5th and 20th days of the month you should write "
                  "'5-20' here.")
    pays_during_holidays = fields.\
        Boolean('Pays During Holidays',
                help="Indicates whether the partner pays during holidays. "
                     "If it doesn''t, it will be taken into account when "
                     "calculating due dates.", default=True)
    holiday_ids = fields.One2many('res.partner.holidays', 'partner_id',
                                  'Holidays')


class ResPartnerHolidays(models.Model):

    _name = 'res.partner.holidays'
    _order = 'start DESC'

    partner_id = fields.Many2one('res.partner', 'Partner', required=True,
                                 ondelete='cascade')
    start = fields.Date('Start', required=True)
    end = fields.Date('End', required=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s - %s' % (record.start, record.end)))
        return result


class AccountPaymentTerm(models.Model):

    _inherit = "account.payment.term"

    def _decode_payment_days(self, days_char):
        # Admit space, dash and comma as separators
        days_char = days_char.replace(' ', '-').replace(',', '-')
        days_char = [x.strip() for x in days_char.split('-') if x]
        days = [int(x) for x in days_char]
        days.sort()
        return days

    def days_in_month(self, date):
        if date.month == 12:
            date = date.replace(day=31)
        else:
            date = date.replace(month=date.month+1, day=1) - timedelta(days=1)
        return date.day

    def next_day(self, date, day):
        if date.day == day:
            return date
        if day < 1:
            day = 1
        if day > self.days_in_month(date):
            day = self.days_in_month(date)
        while True:
            date += timedelta(days=1)
            if date.day == day:
                return date

    def _after_holidays(self, cr, uid, partner, date, days):
        for holidays in partner.holiday_ids:
            start = datetime.\
                strptime(datetime.strptime(holidays.start, '%Y-%m-%d').
                         strftime(date.strftime('%Y') + '-%m-%d'), '%Y-%m-%d')
            end = datetime.\
                strptime(datetime.strptime(holidays.end, '%Y-%m-%d').
                         strftime(date.strftime('%Y') + '-%m-%d'), '%Y-%m-%d')
            if date >= start and date <= end:
                date = end + timedelta(days=1)
            found = False
            for day in days:
                if date.day <= day:
                    date = self.next_day(date, day)
                    found = True
                    break
            if days and not found:
                date = self.next_day(date, days[0])
        return date.strftime('%Y-%m-%d')

    def compute(self, cr, uid, id, value, date_ref=False, context=None):
        result = super(AccountPaymentTerm, self).compute(cr, uid, id, value,
                                                         date_ref, context)
        if not context.get('partner_id'):
            return result
        partner = self.pool.get('res.partner').\
            browse(cr, uid, context.get('partner_id'), context)
        if not partner.payment_days:
            return result

        days = self._decode_payment_days(partner.payment_days)

        new_result = []
        for line in result:
            new_date = False
            date = datetime.strptime(line[0], '%Y-%m-%d')

            for day in days:
                if date.day <= day:
                    new_date = self.next_day(date, day)
                    break

            if days:
                if not new_date:
                    day = days[0]
                    date = self.next_day(date, day)
                else:
                    date = new_date

            if not partner.pays_during_holidays:
                date = self._after_holidays(cr, uid, partner, date, days)

            new_result.append((date, line[1]))

        return new_result
