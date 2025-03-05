from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    last_payment_date = fields.Date(
        string='Last Payment Date',
        compute='_compute_last_payment_date',
        store=True,
        help='Shows the date of the last payment made for this invoice'
    )

    @api.depends('payment_state')
    def _compute_last_payment_date(self):
        for invoice in self:
            if invoice.payment_state == 'paid' and invoice.invoice_payments_widget:
                payment_data = invoice.invoice_payments_widget.get('content', [])
                if payment_data:
                    last_payment = max(payment_data, key=lambda x: x['date'])
                    invoice.last_payment_date = last_payment['date']
                else:
                    invoice.last_payment_date = False
            else:
                invoice.last_payment_date = False
