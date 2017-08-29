# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _get_journal(self):
        journals = self.env['account.journal'].search([('type', '=', 'sale')])
        return journals and journals[0] or False

    journal = fields.Many2one('account.journal', default=_get_journal)

    @api.multi
    def create_invoices(self):
        return super(
            SaleAdvancePaymentInv,
            self.with_context(default_journal_id=self.journal)
        ).create_invoices()
