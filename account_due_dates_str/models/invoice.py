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

from odoo import models, fields, api
from odoo.tools import formatLang, format_date
import math


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    def get_expiration_dates_list(self):
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
                        self.env, line.debit, currency_obj=currency)
                else:
                    quantity = formatLang(self.env, line.credit)
                expiration_dates.append('{} -------------> {}'.format(
                    format_date(self.env, line.date_maturity), quantity))
        return expiration_dates

    def get_expiration_dates_tuples(self):
        self.ensure_one()
        expiration_date_list = []
        expiration_dates = self.get_expiration_dates_list()
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
            expiration_dates = invoice.get_expiration_dates_list()
            invoice.expiration_dates_str = '\n'.join(expiration_dates)

    expiration_dates_str = fields.Text('Expiration dates', readonly=True,
                                       compute='_compute_expiration_dates_str')
