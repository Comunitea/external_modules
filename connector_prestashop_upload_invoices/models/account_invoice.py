# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, models
from odoo.exceptions import UserError


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    def action_invoice_open(self):
        res = super().action_invoice_open()
        for invoice in self:
            if invoice.type == "out_invoice" and invoice.mapped(
                "invoice_line_ids.sale_line_ids.order_id.prestashop_bind_ids"
            ):

                report = self.env.ref("account.account_invoices")
                if report.report_type in ["qweb-html", "qweb-pdf"]:
                    result, format = report.render_qweb_pdf([invoice.id])
                else:
                    res = report.render([invoice.id])
                    if not res:
                        raise UserError(
                            _("Unsupported report type %s found.")
                            % report.report_type
                        )
                    result, format = res
                for sale_bind in invoice.mapped(
                    "invoice_line_ids.sale_line_ids.order_id.prestashop_bind_ids"
                ):
                    if not sale_bind.backend_id.invoice_report_folder:
                        continue
                    report_name = sale_bind.name
                    ext = "." + format
                    if not report_name.endswith(ext):
                        report_name += ext
                    with open(
                        "{}/{}".format(
                            sale_bind.backend_id.invoice_report_folder,
                            report_name,
                        ),
                        "wb",
                    ) as f:
                        f.write(result)
        return res
