# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import io
from ftplib import FTP, FTP_TLS

import paramiko

from odoo import _, models
from odoo.exceptions import UserError


class PrestashopSaleOrder(models.Model):
    _inherit = "prestashop.sale.order"

    def _get_prestashop_report_name(self):
        self.ensure_one()
        return self.name


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _upload_invoices_to_prestashop(self):
        self.ensure_one()
        report = self.env.ref("account.account_invoices_without_payment")
        if report.report_type in ["qweb-html", "qweb-pdf"]:
            result, format = report._render_qweb_pdf(self.sudo().invoice_ids._ids)
        else:
            res = report._render(self.sudo().invoice_ids._ids)
            if not res:
                raise UserError(
                    _("Unsupported report type %s found.") % report.report_type
                )
            result, format = res
        for sale_bind in self.prestashop_bind_ids:
            if not sale_bind.backend_id.ftp_report_folder:
                continue
            report_name = sale_bind._get_prestashop_report_name()
            ext = "." + format
            if not report_name.endswith(ext):
                report_name += ext
            if sale_bind.backend_id.ftp_protocol == "sftp":
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
            elif sale_bind.backend_id.ftp_protocol in ("ftps", "ftp"):
                if sale_bind.backend_id.ftp_protocol == "ftps":
                    ftp = FTP_TLS()
                else:
                    ftp = FTP()
                ftp.connect(
                    sale_bind.backend_id.ftp_host, sale_bind.backend_id.ftp_port
                )
                ftp.login(
                    sale_bind.backend_id.ftp_user, sale_bind.backend_id.ftp_password
                )
                if sale_bind.backend_id.ftp_secure_data_connection:
                    ftp.prot_p()
                ftp.cwd(sale_bind.backend_id.ftp_report_folder)
                ftp.storbinary("STOR " + report_name, io.BytesIO(result))
                ftp.quit()
