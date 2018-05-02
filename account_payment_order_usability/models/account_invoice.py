# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, _, fields
from odoo.exceptions import UserError


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    @api.multi
    def _get_in_payment_order(self):
        aplo = self.env['account.payment.line']
        for inv in self:
            res = True
            if inv.state == 'open' and inv.move_id and inv.payment_order_ok:
                for line in inv.move_id.line_ids:
                    if (line.account_id == inv.account_id and not
                            line.reconciled):
                        if inv.returned_payment:
                            domain = [('move_line_id', '=', line.id),
                                      ('state', 'not in', ['cancel',
                                                           'uploaded'])]
                        else:
                            domain = [('move_line_id', '=', line.id),
                                      ('state', '!=', 'cancel')]
                        paylines = aplo.search(domain)
                        if not paylines:
                            res = False
                            break
                inv.in_payment_order = res

    @api.model
    def _search_in_payment_order(self, operator, value):
        if operator != '=' or value not in (True, False):
            raise ValueError(_("Unsupported search operator"))
        aplo = self.env['account.payment.line']
        domain = [('state', 'not in', ['cancel', 'uploaded'])]
        paylines = aplo.search(domain)
        invoices = paylines.mapped('move_line_id.stored_invoice_id')
        if not value:
            return [('id', 'not in', invoices.ids)]
        else:
            return [('id', 'in', invoices.ids)]

    in_payment_order = fields.Boolean("In payment order",
                                      compute="_get_in_payment_order",
                                      search="_search_in_payment_order")

    @api.multi
    def create_account_payment_line(self):
        for inv in self:
            if inv.payment_order_ok and not inv.mandate_id:
                raise UserError(_(
                    "No Mandate on invoice %s") % inv.number)
        return super(AccountInvoice, self).create_account_payment_line()
