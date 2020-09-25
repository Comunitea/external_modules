# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    def action_invoice_open(self):
        res = super().action_invoice_open()
        for invoice in self:
            if (
                invoice.type in ("out_invoice", "out_refund")
                and invoice.mapped(
                    "invoice_line_ids.sale_line_ids.order_id.prestashop_bind_ids"
                )
                and invoice.state in ("open", "paid")
            ):
                invoice.mapped(
                    "invoice_line_ids.sale_line_ids.order_id"
                ).with_delay()._upload_invoices_to_prestashop()
        return res
