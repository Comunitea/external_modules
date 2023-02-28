# © 2023 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, _
from odoo.exceptions import UserError
import base64


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def new_invoice_from_payment_return(self):
        # new_invoice = self.copy({
        #     'origin': _("Return charges %s") % self.name,
        #     'invoice_line_ids': False
        # })
        new_invoice = self.env['account.invoice'].create({
            'origin': _("Return charges %s") % self.name,
            'partner_id': self.partner_id.id,
            'type': 'out_invoice',
            'fiscal_position_id': self.fiscal_position_id.id,
        })
        return_product = self.company_id.expense_product_id

        if not return_product:
            raise UserError(
                _('Not Expense product found configured in company'))

        account = return_product.property_account_income_id or \
            return_product.categ_id.property_account_income_categ_id

        if not account and return_product:
            raise UserError(_('Please define income account for this product: \
                              "%s"  or for its category: "%s".') %
                (return_product.name, return_product.categ_id.name))
        

        charge_price = self.amount_total * \
            (self.journal_id.payment_return_charge / 100)
        if charge_price < self.journal_id.min_charge:
            charge_price = self.journal_id.min_charge

        vals = {
            'product_id': return_product.id,
            'quantity': 1,
            'price_unit': charge_price,
            'invoice_id': new_invoice.id,
            'name': return_product.name,
            'account_id': account.id,
        }
        # line = self.env['account.invoice.line'].new(vals)
        line = self.env['account.invoice.line'].create(vals)
        line._onchange_product_id()
        line.price_unit = charge_price
        # line._compute_price()
        # new_values = line._convert_to_write(line._cache)
        # ll = self.env['account.invoice.line'].create(new_values)
        new_invoice._onchange_invoice_line_ids()
        return new_invoice

    def send_payment_returned_mail(self):
        self.ensure_one()

        new_invoice = self.new_invoice_from_payment_return()
        new_invoice.with_context(
            bypass_risk=True).action_invoice_open()

        template = self.env.ref(
            'payment_return_invoice_resend.email_template_returned_invoice')
        report_invoice = self.env.ref('account.account_invoices')

        # Attachment Original Invoice
        report_rendered = report_invoice.render_qweb_pdf(self.id)
        data_record = base64.encodestring(report_rendered[0])
        ir_values = {
            'name': 'Invoice %s.pdf' % self.name,
            'type': 'binary',
            'datas': data_record,
            'datas_fname': 'Invoice %s.pdf' % self.name,
            'mimetype': 'application/pdf',
            'res_model': 'mail.compose.message',
            'res_id': 0,
        }
        data_id = self.env['ir.attachment'].create(ir_values)

        # Attachment New Invoice With charges
        report_rendered2 = report_invoice.render_qweb_pdf(new_invoice.id)
        data_record2 = base64.encodestring(report_rendered2[0])
        ir_values = {
            'name': 'Invoice %s.pdf' % self.name,
            'type': 'binary',
            'datas': data_record2,
            'datas_fname': 'Invoice %s.pdf' % self.name,
            'mimetype': 'application/pdf',
            'res_model': 'mail.compose.message',
            'res_id': 0,
        }
        data2_id = self.env['ir.attachment'].create(ir_values)


        ctx = dict(
            default_model='account.invoice',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            user_id=self.env.user.id,
        )
        composer_id = self.env["mail.compose.message"].sudo().\
            with_context(ctx).create({})
        values = composer_id.onchange_template_id(
            template.id, "comment", 'account.invoice', self.id
        )["value"]
        composer_id.write(values)




        if data_id:
            composer_id.attachment_ids = [(6,0, [data_id.id, data2_id.id])]
        composer_id.with_context(ctx).send_mail()
        return new_invoice
