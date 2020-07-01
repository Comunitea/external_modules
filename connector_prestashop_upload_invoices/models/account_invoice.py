# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import paramiko
import io
from odoo import _, models
from odoo.exceptions import UserError
from odoo.addons.queue_job.job import job


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    def action_invoice_open(self):
        res = super().action_invoice_open()
        for invoice in self:
            if invoice.type == "out_invoice" and invoice.mapped(
                "invoice_line_ids.sale_line_ids.order_id.prestashop_bind_ids"
            ):

                invoice.with_delay()._upload_report_to_prestashop()
        return res

    @job(default_channel='root.prestashop')
    def _upload_report_to_prestashop(self):
        self.ensure_one()
        report = self.env.ref("account.account_invoices_without_payment")
        if report.report_type in ["qweb-html", "qweb-pdf"]:
            result, format = report.render_qweb_pdf([self.id])
        else:
            res = report.render([self.id])
            if not res:
                raise UserError(
                    _("Unsupported report type %s found.")
                    % report.report_type
                )
            result, format = res
        for sale_bind in self.mapped("invoice_line_ids.sale_line_ids.order_id.prestashop_bind_ids"):
            if not sale_bind.backend_id.ftp_report_folder:
                continue
            report_name = sale_bind.name
            ext = "." + format
            if not report_name.endswith(ext):
                report_name += ext
            transport = paramiko.Transport((sale_bind.backend_id.ftp_host, sale_bind.backend_id.ftp_port))
            transport.connect(None, sale_bind.backend_id.ftp_user, sale_bind.backend_id.ftp_password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.chdir(sale_bind.backend_id.ftp_report_folder)
            sftp.putfo(io.BytesIO(result), report_name)
            sftp.close()
