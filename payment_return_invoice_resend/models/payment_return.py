# © 2023 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _


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
        msg = "<h2>Facturas devueltas y gastos devolución:</h2> <ul>"
        for inv in invoices.filtered(lambda l: l.state == 'open'):
            retun_invoice = inv.send_payment_returned_mail()
            inv_link =  "<a href=# data-oe-model=account.invoice data-oe-id=%d>%s</a>" % (inv.id, inv.number)
            inv_link2 = "<a href=# data-oe-model=account.invoice data-oe-id=%d>%s</a>" % (retun_invoice.id, retun_invoice.number)
            msg += "<li>Factura: {} => Factura Gastos: {}</li>".format(inv_link, inv_link2)
        msg += "</ul>"
        self.message_post(body=msg, subject=_("Invoices Returned"))