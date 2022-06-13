# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class AccountMove(models.Model):

    _inherit = "account.move"

    def _post(self):
        res = super()._post()
        for move in self:
            if (
                move.move_type in ("out_invoice", "out_refund")
                and move.mapped(
                    "invoice_line_ids.sale_line_ids.order_id.prestashop_bind_ids"
                )
                and move.state == "posted"
            ):
                move.mapped(
                    "invoice_line_ids.sale_line_ids.order_id"
                ).with_delay()._upload_invoices_to_prestashop()
        return res
