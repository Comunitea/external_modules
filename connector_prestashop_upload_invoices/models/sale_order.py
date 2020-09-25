# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import io

import paramiko
from odoo import _, models
from odoo.addons.queue_job.job import job
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @job(default_channel="root.prestashop")
    def _upload_invoices_to_prestashop(self):
        self.ensure_one()
        report = self.env.ref("account.account_invoices_without_payment")
        if report.report_type in ["qweb-html", "qweb-pdf"]:
            result, format = report.render_qweb_pdf(self.invoice_ids._ids)
        else:
            res = report.render(self.invoice_ids._ids)
            if not res:
                raise UserError(
                    _("Unsupported report type %s found.") % report.report_type
                )
            result, format = res
        for sale_bind in self.prestashop_bind_ids:
            if not sale_bind.backend_id.ftp_report_folder:
                continue
            report_name = sale_bind.name
            ext = "." + format
            if not report_name.endswith(ext):
                report_name += ext
            transport = paramiko.Transport(
                (sale_bind.backend_id.ftp_host, sale_bind.backend_id.ftp_port)
            )
            transport.connect(
                None,
                sale_bind.backend_id.ftp_user,
                sale_bind.backend_id.ftp_password,
            )
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.chdir(sale_bind.backend_id.ftp_report_folder)
            sftp.putfo(io.BytesIO(result), report_name)
            sftp.close()
