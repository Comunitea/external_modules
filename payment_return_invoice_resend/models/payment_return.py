# © 2023 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class PaymentReturn(models.Model):
    _inherit = "payment.return"

    @api.multi
    def action_confirm(self):
        res = super().action_confirm()
        if self.state == 'done':
            self.resend_open_invoices()
        return res
    
    def resend_open_invoices(self):
        self.ensure_one()
        invoices = self.line_ids.mapped('move_line_ids.matched_debit_ids.origin_returned_move_ids.invoice_id')
        for inv in invoices.filtered(lambda l: l.state == 'open'):
            inv.send_payment_returned_mail()