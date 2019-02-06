# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, exceptions, _


class ComputeRappelInvoice(models.TransientModel):

    _name = "rappel.invoice.wzd"

    journal_id = fields.Many2one("account.journal", "Journal", required=True,
                                 domain=[("type", '=', "sale")])
    invoice_date = fields.Date()
    group_by_partner = fields.Boolean()

    @api.multi
    def action_invoice(self):
        invoices = []
        compute_rappel_obj = self.env["rappel.calculated"]
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        partner_group = {}
        for rappel in compute_rappel_obj.\
                browse(self.env.context["active_ids"]):
            if rappel.quantity <= 0:
                continue
            if rappel.invoice_id:
                raise exceptions.Warning(_("The rappel %s of %s with period"
                                           " %s - %s is already invoiced") %
                                         (rappel.rappel_id.name,
                                          rappel.partner_id.name,
                                          rappel.date_start, rappel.date_end))
            else:
                if self[0].group_by_partner and \
                        partner_group.get(rappel.partner_id.id):
                    invoice = partner_group[rappel.partner_id.id]
                else:
                    fpos = rappel.partner_id.property_account_position_id
                    invoice_vals = {'partner_id': rappel.partner_id.id,
                                    'date_invoice': self[0].invoice_date or
                                    False,
                                    'journal_id': self[0].journal_id.id,
                                    'account_id': rappel.partner_id.
                                    property_account_receivable_id.id,
                                    'type': 'out_refund',
                                    'fiscal_position_id': fpos and fpos.id or
                                    False}
                    invoice = invoice_obj.create(invoice_vals)
                    invoices.append(invoice.id)
                    if self[0].group_by_partner:
                        partner_group[rappel.partner_id.id] = invoice
                rappel.invoice_id = invoice.id
                rappel_product = rappel.rappel_id.type_id.product_id
                account_id = rappel_product.property_account_income_id
                if not account_id:
                    account_id = rappel_product.categ_id.\
                        property_account_income_categ_id
                taxes_ids = rappel_product.taxes_id
                fpos = rappel.partner_id.property_account_position_id or False
                if fpos:
                    account_id = fpos.map_account(account_id)
                    taxes_ids = fpos.map_tax(taxes_ids)
                tax_ids = [(6, 0, [x.id for x in taxes_ids])]

                invoice_line_obj.create({'product_id': rappel_product.id,
                                         'name': '%s (%s-%s)' %
                                                 (rappel.rappel_id.name,
                                                  rappel.date_start,
                                                  rappel.date_end),
                                         'invoice_id': invoice.id,
                                         'account_id': account_id.id,
                                         'invoice_line_tax_ids': tax_ids,
                                         'price_unit': rappel.quantity,
                                         'quantity': 1})

        if not invoices:
            raise exceptions.Warning(_('Any invoice created!'))

        action = self.env.ref('account.action_invoice_out_refund')
        if action:
            action = action.read([])[0]
            action['domain'] = str([('id', 'in', invoices)])
            return action
        return True
