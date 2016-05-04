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

from openerp import models, fields, api, _
from openerp.exceptions import Warning
import time


class StockPicking(models.Model):

    _inherit = "stock.picking"

    pending_invoice_move_id = fields.Many2one('account.move',
                                              'Account pending move',
                                              readonly=True,
                                              copy=False)

    @api.one
    def account_pending_invoice(self):
        period_obj = self.env['account.period']
        move_obj = self.env['account.move']
        product_uom_obj = self.env['product.uom']
        move_line_obj = self.env['account.move.line']

        amount = 0
        date = self.min_date and self.min_date[:10] or \
            time.strftime('%Y-%m-%d')
        period_id = period_obj.find(date)

        origin = self.name
        if self.origin:
            origin += ':' + self.origin

        stock_journal_id = self.company_id.property_pending_stock_journal.id

        move = {
            'ref': origin,
            'journal_id': stock_journal_id,
            'period_id': period_id.id,
            'date': date,
        }
        move_id = move_obj.create(move)
        obj_precision = self.env['decimal.precision']
        for move_line in self.move_lines:
            # Get expense account
            account_id = move_line.product_id.product_tmpl_id.\
                property_account_expense.id
            if not account_id:
                account_id = move_line.product_id.categ_id.\
                    property_account_expense_categ.id

            name = move_line.name or origin
            if move_line.purchase_line_id:
                unit_price_line = move_line.purchase_line_id.price_unit
                discount_line = move_line.purchase_line_id.discount or 0.0
            else:
                unit_price_line = move_line.product_id.standard_price
                discount_line = 0

            # Convertir a unidad de medida
            unit_price_line = product_uom_obj._compute_price(
                move_line.product_uom.id, unit_price_line,
                move_line.product_id.uom_id.id )

                #raise Warning("There is no purchase line related. Can not "
                #              "calculate price for accounting pending
            # invoice")

            price_line = unit_price_line * (1 - (discount_line or 0.0) / 100.0)
            price_line = price_line * move_line.product_qty
            amount_line = round(price_line,
                                obj_precision.precision_get('Account'))
            if move_line.purchase_line_id and (
                    move_line.purchase_line_id.order_id.currency_id !=
                        move_line.company_id.currency_id):
                from_currency = move_line.purchase_line_id.order_id.currency_id
                to_currency = move_line.company_id.currency_id
                amount_line = from_currency.compute(amount_line, to_currency)

            amount += amount_line
            vals = {
                'name': name,
                'ref': origin,
                'partner_id': self.partner_id.commercial_partner_id.id,
                'product_id': move_line.product_id.id,
                'account_id': account_id,
                'debit': amount_line,
                'credit': 0,
                'quantity': move_line.product_qty,
                'move_id': move_id.id,
                'journal_id': stock_journal_id,
                'period_id': period_id.id,
            }
            move_line_obj.create(vals)

        account_id = self.company_id.\
            property_pending_supplier_invoice_account.id
        vals = {
            'name': name,
            'ref': origin,
            'partner_id': self.partner_id.commercial_partner_id.id,
            'account_id': account_id,
            'debit': 0,
            'credit': amount,
            'move_id': move_id.id,
            'journal_id': stock_journal_id,
            'period_id': period_id.id,
        }

        move_line_obj.create(vals)
        move_id.post()

        self.pending_invoice_move_id = move_id

        return move_id

    @api.multi
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if vals.get('date_done', False):
            for pick in self:
                exists_purchase = False
                for move in pick.move_lines:
                    if move.purchase_line_id:
                        exists_purchase = True
                        break
                if (pick.picking_type_id.code == "incoming" and
                        exists_purchase and
                        pick.invoice_state in ['invoiced', '2binvoiced'] and
                        pick.company_id.required_invoice_pending_move):
                    pick.refresh()
                    if not pick.company_id.\
                            property_pending_supplier_invoice_account:
                        raise Warning(_("You need to configure an account "
                                        "in the company for pending invoices"))
                    if not pick.company_id.property_pending_stock_journal:
                        raise Warning(_("You need to configure an account "
                                        "journal in the company for pending "
                                        "invoices"))
                    pick.account_pending_invoice()
        return res
