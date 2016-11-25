# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea Servicios Tecnológicos All Rights Reserved
#    $Omar Castiñeira Saaevdra <omar@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ResPartnerRappelRel(models.Model):

    _name = "res.partner.rappel.rel"
    _rec_name = "partner_id"

    PERIODICITIES = [('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
                     ('semiannual', 'Semiannual'), ('annual', 'Annual')]
    PERIODICITIES_MONTHS = {'monthly': 1, 'quarterly': 3, 'semiannual': 6,
                            'annual': 12}

    partner_id = fields.Many2one("res.partner", "Customer", required=True,
                                 domain=[("customer", "=", True),
                                         ("is_company", '=', True)])
    rappel_id = fields.Many2one("rappel", "Rappel", required=True)
    date_start = fields.Date("Start date", required=True,
                             default=fields.Date.context_today)
    date_end = fields.Date("End date")
    periodicity = fields.Selection(PERIODICITIES, "Periodicity",
                                   default="annual", required=True)
    last_settlement_date = fields.Date("Last settlement date")

    @api.multi
    def _get_next_period(self):
        self.ensure_one()
        if self.last_settlement_date and \
                self.last_settlement_date > self.date_start:
            date_start = \
                datetime.strptime(self.last_settlement_date, '%Y-%m-%d').date()
        else:
            date_start = \
                datetime.strptime(self.date_start, '%Y-%m-%d').date()

        date_stop = date_start + \
            relativedelta(months=self.PERIODICITIES_MONTHS[self.periodicity],
                          days=-1)
        if self.date_end:
            date_end = datetime.strptime(self.date_end, '%Y-%m-%d').date()
            if date_end < date_stop:
                date_stop = date_end

        if date_start != date_stop:
            period = [date_start, date_stop]
        else:
            period = False

        return period

    @api.multi
    def _get_invoices(self, period, products):
        self.ensure_one()
        invoices = self.env['account.invoice'].search(
            [('type', '=', 'out_invoice'),
             ('date_invoice', '>=', period[0]),
             ('date_invoice', '<=', period[1]),
             ('state', 'in', ['open', 'paid']),
             ('partner_id', '=', self.partner_id.id)])
        refunds = self.env['account.invoice'].search(
            [('type', '=', 'out_refund'),
             ('date_invoice', '>=', period[0]),
             ('date_invoice', '<=', period[1]),
             ('state', 'in', ['open', 'paid']),
             ('partner_id', '=', self.partner_id.id)])

        # se buscan las rectificativas
        refund_lines = self.env['account.invoice.line'].search(
            [('invoice_id', 'in', [x.id for x in refunds]),
             ('product_id', 'in', products),
             ('no_rappel', '=', False)])
        invoice_lines = self.env['account.invoice.line'].search(
            [('invoice_id', 'in', [x.id for x in invoices]),
             ('product_id', 'in', products),
             ('no_rappel', '=', False)])
        return invoice_lines, refund_lines

    @api.model
    def compute(self, period, invoice_lines, refund_lines, tmp_model=False):
        for rappel in self:
            rappel_info = {'rappel_id': rappel.rappel_id.id,
                           'partner_id': rappel.partner_id.id,
                           'date_start': period[0],
                           'amount' :0.0,
                           'date_end': period[1]}
            total_rappel = 0.0
            if rappel.rappel_id.calc_mode == 'fixed':
                if rappel.rappel_id.calc_amount == 'qty':
                    total_rappel = rappel.rappel_id.fix_qty
                else:
                    total = sum([x.price_subtotal for x in invoice_lines]) - \
                        sum([x.price_subtotal for x in refund_lines])
                    if total:
                        total_rappel = total * rappel.rappel_id.fix_qty / 100.0
                    rappel_info["curr_qty"] = total

                rappel_info['amount'] = total_rappel
            else:
                field = ''
                if rappel.rappel_id.qty_type == 'value':
                    field = 'price_subtotal'
                else:
                    field = 'quantity'
                total = sum([x[field] for x in invoice_lines]) - \
                    sum([x[field] for x in refund_lines])
                rappel_info["curr_qty"] = total
                if total:
                    section = self.env['rappel.section'].search(
                        [('rappel_id', '=', rappel.rappel_id.id),
                         ('rappel_from', '<=', total),
                         ('rappel_until', '>=', total)])
                    if not section:
                        section = self.env['rappel.section'].search(
                            [('rappel_id', '=', rappel.rappel_id.id),
                             ('rappel_from', '<=', total),
                             ('rappel_until', '=', False)],
                            order='rappel_from desc', limit=1)
                    if not section:
                        rappel_info['amount'] = 0.0
                    else:
                        rappel_info['section_id'] = section.id
                        section = section[0]
                        if rappel.rappel_id.calc_amount == 'qty':
                            total_rappel = section.percent
                        else:
                            total_rappel = total * \
                                section.percent / 100.0
                            rappel_info['amount'] = total_rappel
                else:
                    rappel_info['amount'] = 0.0

            if period[1] <= fields.Date.from_string(fields.Date.today()):
                if total_rappel:
                    self.env['rappel.calculated'].create({
                        'partner_id': rappel.partner_id.id,
                        'date_start': period[0],
                        'date_end': period[1],
                        'quantity': total_rappel,
                        'rappel_id': rappel.rappel_id.id
                    })
                rappel.last_settlement_date = period[1]
            else:
                if tmp_model and rappel_info:
                    self.env['rappel.current.info'].create(rappel_info)

        return True
