# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields
import base64
import requests
from .cex_request import CexRequest


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    carrier_type = fields.Selection(selection_add=[("cex", "Correos Express")])
    cex_account = fields.Char(string="Correos Express Account")
    cex_password = fields.Char(string="Correos Express Password")
    cex_codRte = fields.Char(string="Correos Express codRte")
    cex_solicitante = fields.Char(string="Correos Express Solicitante")

    def cex_get_tracking_link(self, picking):
        return "https://s.correosexpress.com/SeguimientoSinCP/search?shippingNumber={}".format(
            picking.carrier_tracking_ref
        )

    def cex_send_shipping(self, pickings):
        return [self.cex_send_shipping(p) for p in pickings]

    def cex_send_shipping(self, picking):
        cex_request = CexRequest(self)
        labels = CexRequest._generate_cex_label(vals)
        for label in labels:
            data = {
                "name": label["name"],
                "datas_fname": label.get("filename", label["name"]),
                "res_id": picking.id,
                "res_model": "stock.picking",
                "datas": label["file"],
                "file_type": label["file_type"],
            }
            if label.get("package_id"):
                data["package_id"] = label["package_id"]
            
            attachment = self.env["ir.attachment"].create(data)
            body = _("Correos Express label for tracking ref {}").format(picking.tracking_ref)
            picking.message_post(body=body, attachments=attachment)

    def cex_tracking_state_update(self, picking):
        """Tracking state update"""
        self.ensure_one()
        if not picking.carrier_tracking_ref:
            return
        cex_request = CexRequest(self)
        cex_request.check_shipment_status(picking)
