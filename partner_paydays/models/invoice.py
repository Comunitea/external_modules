# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 NaN Projectes de Programari Lliure, S.L.
#                       http://www.NaN-tic.com
#    Copyright (C) 2016 Comunitea Servicios Tecnológicos, S.L.
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

from odoo import models, api, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):
        date_invoice = self.date_invoice
        if not date_invoice:
            date_invoice = fields.Date.context_today(self)
        if not self.payment_term_id:
            # When no payment term defined
            self.date_due = self.date_due or self.date_invoice
        else:
            pterm = self.payment_term_id
            pterm_list = pterm.\
                with_context(currency_id=self.company_id.currency_id.id,
                             partner_id=self.partner_id.
                             commercial_partner_id.id).\
                compute(value=1, date_ref=date_invoice)[0]
            self.date_due = max(line[0] for line in pterm_list)

    @api.multi
    def action_move_create(self):
        for inv in self:
            ctx = dict(self._context, partner_id=inv.partner_id.
                       commercial_partner_id.id)
            super(AccountInvoice, inv.
                  with_context(ctx)).action_move_create()
        return True
