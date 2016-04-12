# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Omar Castiñeira Saavedra <omar@comunitea.com>$
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

from openerp import models, api
import time


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    @api.multi
    def action_cancel(self):
        ret = super(AccountInvoice, self).action_cancel()
        if ret:
            move_line_obj = self.env['account.move.line']
            lines_to_unreconcile = self.env['account.move.line']
            for inv in self:
                for picking in inv.picking_ids:
                    if picking.pending_invoice_move_id:
                        if picking.pending_invoice_move_id.reversal_id:
                            move_line_ids = move_line_obj.\
                                search([('move_id', '=',
                                         picking.pending_invoice_move_id.id),
                                        ('reconcile_id', '!=', None)])
                            lines_to_unreconcile += move_line_ids[0]
                            if move_line_ids:
                                move_line_rev_ids = move_line_obj.\
                                    search([('move_id', '=',
                                             picking.pending_invoice_move_id.
                                             reversal_id.id),
                                            ('reconcile_id', '!=', None)])
                                lines_to_unreconcile += move_line_rev_ids[0]
                                unrecl = [x.id for x in lines_to_unreconcile]
                                move_line_obj.\
                                    _remove_move_reconcile(move_ids=unrecl)
                                picking.pending_invoice_move_id.reversal_id.\
                                    button_cancel()
                                picking.pending_invoice_move_id.reversal_id.\
                                    unlink()

        return ret

    @api.multi
    def action_move_create(self):
        ret = super(AccountInvoice, self).action_move_create()
        if ret:
            move_line_obj = self.env['account.move.line']
            move_obj = self.env['account.move']

            for inv in self:
                for picking in inv.picking_ids:
                    lines_to_reconcile = self.env['account.move.line']
                    if picking.pending_invoice_move_id:
                        date = inv.date_invoice or time.strftime('%Y-%m-%d')
                        acc_id = inv.company_id.\
                            property_pending_supplier_invoice_account.id
                        line_ids = move_line_obj.\
                            search([('move_id', '=',
                                     picking.pending_invoice_move_id.id),
                                    ('account_id', '=', acc_id)])
                        lines_to_reconcile += line_ids[0]
                        move_rev = picking.pending_invoice_move_id.\
                            create_reversals(date)
                        move_rev = move_obj.browse(move_rev[0])
                        move_rev.post()
                        # Reconcile
                        line_rev_ids = move_line_obj.\
                            search([('move_id', '=', move_rev.id),
                                    ('account_id', '=', acc_id)])
                        lines_to_reconcile += line_rev_ids[0]

                        amount = 0.0
                        for rline in lines_to_reconcile:
                            amount += rline.debit - rline.credit

                        currency = inv.currency_id
                        if currency.is_zero(amount):
                            lines_to_reconcile.reconcile('payment')
                        else:
                            lines_to_reconcile.reconcile_partial('payment')

        return ret
