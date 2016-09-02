# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego (<http://www.pexego.es>).
#
#    All other contributions are (C) by their respective contributors
#
#    All Rights Reserved
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
from lxml import etree


class account_invoice(models.Model):

    _inherit = "account.invoice"

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False,
                        submenu=False):
        context = self._context

        res = super(account_invoice, self).fields_view_get(view_id=view_id,
                                                           view_type=view_type,
                                                           toolbar=toolbar,
                                                           submenu=submenu)

        doc = etree.XML(res['arch'])

        if context.get('type'):
            for node in doc.xpath("//field[@name='partner_bank_id']"):
                if context['type'] in ('in_refund', 'out_refund'):
                    node.set('domain', """['|','|',('partner_id.ref_companies',
'in', [company_id]),('partner_id', '=', partner_id),('partner_id.child_ids',
'child_of', [partner_id])]""")

        res['arch'] = etree.tostring(doc)
        return res

    @api.multi
    def onchange_partner_id(
            self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        res = super(account_invoice, self).onchange_partner_id(
            type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if type == 'out_invoice' and partner.customer_payment_mode and \
                    partner.customer_payment_mode.\
                    payment_order_type == "debit" and partner.bank_ids:
                mandate_obj = self.env["account.banking.mandate"]
                mandates = mandate_obj.\
                    search([('partner_bank_id', 'in', partner.bank_ids.ids),
                            ('default', '=', True),('state', '=', 'valid')])
                mandate_sel = False
                if mandates:
                    mandate_sel = mandates[0]
                else:
                    mandates = mandate_obj.\
                        search([('partner_bank_id', 'in',
                                 partner.bank_ids.ids),
                                ('state', '=', 'valid')])
                    if mandates:
                        mandate_sel = mandates[0]
                if mandate_sel:
                    res['value'].\
                        update({'mandate_id': mandate_sel.id,
                                'partner_bank_id':
                                mandate_sel.partner_bank_id.id})
                else:
                    res['value'].\
                        update({'partner_bank_id':
                                partner.bank_ids[0].id})
        return res

    @api.model
    def create(self, vals):
        if vals.get('partner_bank_id', False) and \
                vals.get('payment_mode_id', False) and not \
                vals.get('sdd_mandate_id', False):
            pmode = self.env["payment.mode"].\
                browse(vals['payment_mode_id'])
            if pmode.payment_order_type == "debit":
                mandate_obj = self.env["account.banking.mandate"]
                mandates = mandate_obj.\
                    search([('partner_bank_id', '=', vals['partner_bank_id']),
                            ('default', '=', True),('state', '=', 'valid')])
                mandate_sel = False
                if mandates:
                    mandate_sel = mandates[0]
                else:
                    mandates = mandate_obj.\
                        search([('partner_bank_id', '=',
                                 vals['partner_bank_id']),
                                ('state', '=', 'valid')])
                    if mandates:
                        mandate_sel = mandates[0]
                if mandate_sel:
                    vals['mandate_id'] = mandate_sel.id

        return super(account_invoice, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('partner_bank_id', False) and not \
                vals.get('sdd_mandate_id', False):
            if vals.get("payment_mode_id", False):
                pmode_id = vals['payment_mode_id']
            else:
                pmode_id = self[0].payment_mode_id.id
            if pmode_id:
                pmode = self.env["payment.mode"].\
                    browse(pmode_id)
                if pmode.payment_order_type == "debit":
                    mandate_obj = self.env["account.banking.mandate"]
                    mandates = mandate_obj.\
                        search([('partner_bank_id', '=',
                                 vals['partner_bank_id']),
                                ('default', '=', True),
                                ('state', '=', 'valid')])
                    mandate_sel = False
                    if mandates:
                        mandate_sel = mandates[0]
                    else:
                        mandates = mandate_obj.\
                            search([('partner_bank_id', '=',
                                     vals['partner_bank_id']),
                                    ('state', '=', 'valid')])
                        if mandates:
                            mandate_sel = mandates[0]
                    if mandate_sel:
                        vals['mandate_id'] = mandate_sel.id

        return super(account_invoice, self).write(vals)
