# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Comunitea (<http://www.comunitea.com>).
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

from openerp import models, api


class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.model
    def _create_invoice_from_picking(self, picking, vals):
        invoice_id = super(StockPicking, self).\
            _create_invoice_from_picking(picking, vals)
        inv_type = self.env.context.get('inv_type', 'out_invoice')
        if picking and picking.sale_id and inv_type == 'out_invoice':
            sale_order = picking.sale_id
            if sale_order.payment_mode_id and sale_order.payment_mode_id.\
                    payment_order_type == "debit":
                invoice = self.env["account.invoice"].browse(invoice_id)
                invoice_partner = invoice.partner_id.commercial_partner_id
                mandate_obj = self.env["account.banking.mandate"]
                mandates = mandate_obj.\
                    search([('partner_bank_id', 'in',
                             invoice_partner.bank_ids.ids),
                            ('default', '=', True),
                            ('state', '=', 'valid')])
                mandate_sel = False
                if mandates:
                    mandate_sel = mandates[0]
                else:
                    mandates = mandate_obj.search(
                        [('partner_bank_id', 'in',
                          invoice_partner.bank_ids.ids),
                         ('state', '=', 'valid')])
                    if mandates:
                        mandate_sel = mandates[0]
                if mandate_sel:
                    invoice.mandate_id = mandate_sel.id,
                    invoice.partner_bank_id = mandate_sel.partner_bank_id.id
                elif invoice_partner.bank_ids:
                    invoice.partner_bank_id = invoice_partner.bank_ids[0].id
        return invoice_id
