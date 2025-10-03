##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2025 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from .nacex_request import NcxRequest


class DeliveryCarrier(models.Model):

    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(selection_add=[("ncx", "NACEX")])
    ncx_account = fields.Char("NACEX Account")
    ncx_password = fields.Char("NACEX Password")
    ncx_client = fields.Char("NACEX Client Code")
    ncx_delegation = fields.Char("NACEX Delegation Code")
    ncx_client_department = fields.Char("NACEX Franchise Code")
    ncx_oldmodel = fields.Boolean(string='Old model')
    ncx_payment_on_delivery = fields.Boolean(string='Payment on delivery', default=False)
    ncx_printer_model = fields.Selection(
        [
            ("TECSV4_B", "TECSV4_B"),
            ("TECEV4_B", "TECEV4_B"),
            ("TECFV4_B", "TECFV4_B"),
            ("ZEBRA_B", "ZEBRA_B"),
            ("IMAGEN_B", "IMAGEN_B"),
        ],
        default="TECSV4_B",
    )
    ncx_payment_type = fields.Selection(
        [
            ("O", "Payment on origin"),
            ("D", "Payment on destination"),
            ("T", "Payment by a third party"),
        ],
        default="O",
    )
    ncx_package_type = fields.Selection(
        [
            ("0", "Documents"),
            ("1", "Nacex Bag"),
            ("2", "Nacex Cardboard Box"),
        ],
        default="2",
    )
    ncx_pod_type = fields.Selection(
        [
            ("N", "No"),
            ("O", "Origin"),
            ("D", "Destination"),
            ("A", "Payment on pick up"),
        ],
        default="D",
    )

    def ncx_get_tracking_link(self, picking):
        return "http://www.nacex.es/irSeguimiento.do?seguimiento={}".format(
            picking.carrier_tracking_ref
        )

    def base64_url_decode(self, label):
        padding_factor = (4 - len(label) % 4) % 4
        label += "="*padding_factor
        return base64.b64decode(str(label).translate(dict(zip(map(ord, u'-_'), u'+/'))))

    def _prepare_ncx_shipping(self, picking):
        self.ensure_one()
        arrayOfString_3 = [
            "del_cli={}".format(self.ncx_delegation),
            "num_cli={}".format(self.ncx_client),
            "tip_ser={}".format(self.carrier_service.carrier_code),
            "tip_cob={}".format(self.ncx_payment_type),
            "ref_cli={}".format(picking.name),
            "tip_env={}".format(self.ncx_package_type),
            "bul={}".format(picking.carrier_packages),
            "kil={}".format(round(picking.carrier_weight)),
            "nom_ent={}".format(picking.partner_id.display_name[:50]),
            "dir_ent={} {}".format(picking.partner_id.street if picking.partner_id.street else '', picking.partner_id.street2 if picking.partner_id.street2 else ''),
            "pais_ent={}".format(picking.partner_id.country_id.code),
            "cp_ent={}".format(picking.partner_id.zip),
            "pob_ent={}".format(picking.partner_id.city),
            "tel_ent={}".format(picking.partner_id.phone if picking.partner_id.phone else picking.partner_id.mobile if picking.partner_id.mobile else ''),
            "obs1={}".format(picking.delivery_note[0:38] if picking.delivery_note else ''),
            "obs2={}".format(picking.delivery_note[38:75] if picking.delivery_note else ''),
            "obs3={}".format(picking.delivery_note[75:113] if picking.delivery_note else ''),
            "obs4={}".format(picking.delivery_note[113:151] if picking.delivery_note else ''),
            "ret={}".format("S" if self.ncx_shipping_return else "N"),
        ]

        if self.ncx_payment_on_delivery and self.ncx_pod_type:
            arrayOfString_3.append("ree={}".format(self.pdo_quantity))
            arrayOfString_3.append("tip_ree={}".format(self.ncx_pod_type))

        putExpedicion = {
            "String_1": self.ncx_account,
            "String_2": self.ncx_password,
            "arrayOfString_3": arrayOfString_3
        }
        return putExpedicion

    def ncx_send_shipping(self, pickings):
        return [self.ncx_create_shipping(p) for p in pickings]

    def ncx_create_shipping(self, picking):
        ncx_request = NcxRequest(self)
        vals = self._prepare_ncx_shipping(picking)
        response = ncx_request.putExpedicion(vals)
        vals.update({"tracking_number": False, "exact_price": 0})
        response_message = self._ncx_check_response(response)
        self._mrw_log_request(mrw_request)
        ncx_tracking_ref = response["carrier_tracking_ref"]
        vals["tracking_number"] = ncx_tracking_ref or ""
        vals["shipment_reference"] = response["shipment_reference"] or ""
        self.ncx_get_label(ncx_tracking_ref, picking)
        return vals

    def _ncx_check_response(self, res):
        if res and res._raw_elements and res._raw_elements[0].text =='ERROR':
            raise UserError(_("Error message: {}").format(res._raw_elements[1].text))
        elif res:
            return {
                "carrier_tracking_ref": res._raw_elements[0].text,
                "shipment_reference": res._raw_elements[1].text,
            }
        else:
            raise UserError(
                _("There was an error connecting to Nacex. Check the connection log.")
            )

    def _ncx_check_cancel_response(self, res, picking):
        if res and res._raw_elements and res._raw_elements[0].text == 'ERROR':
            msg = _("Access error message: {}").format(res._raw_elements[0].text)
            raise AccessError(msg)
        elif res and res._raw_elements and res._raw_elements[0].text:
            msg = _("Expedition with number %s cancelled: %s") % (picking.carrier_tracking_ref, res._raw_elements[0].text)
            picking.message_post(body=msg)
        else:
            msg = _("Access error")
            raise AccessError(msg)

    @api.model
    def _ncx_log_request(self, ncx_request):
        ncx_last_request = ncx_last_response = False
        try:
            ncx_last_request = etree.tostring(
                ncx_request.history.last_sent["envelope"],
                encoding="UTF-8",
                pretty_print=True,
            )
            ncx_last_response = etree.tostring(
                ncx_request.history.last_received["envelope"],
                encoding="UTF-8",
                pretty_print=True,
            )
        # Don't fail hard on this. Sometimes zeep could not be able to keep history
        except Exception:
            return
        # Debug must be active in the carrier
        self.log_xml(ncx_last_request, "ncx_request")
        self.log_xml(ncx_last_response, "ncx_response")

    def ncx_get_label(self, ncx_tracking_ref, picking):
        self.ensure_one()
        if not ncx_tracking_ref:
            return False
        vals = self._prepare_label(ncx_tracking_ref)
        ncx_request = NcxRequest(self)
        label = ncx_request.getEtiqueta(vals)
        if label and label[0] != "ERROR":
            if self.ncx_printer_model == "IMAGEN_B":
                file_b64 = self.base64_url_decode(label)

                attachment_values = {
                    "name": "Label: {}".format(picking.name),
                    "type": "binary",
                    "datas": base64.b64encode(file_b64),
                    "datas_fname": "Label" + picking.name + ".png",
                    "store_fname": picking.name,
                    "res_model": picking._name,
                    "res_id": picking.id,
                    "mimetype": "image/png",
                }

            else:
                # We need to replace blank spaces with line breaks
                label_text = ''
                for line in label:
                    if len(line) > 64 and self.ncx_oldmodel:
                        line = line.split("=")[0] + '=' + line.split("=")[1].replace('|', '').replace('}', '')[:29] + '|}'
                    label_text += re.sub('[^!-~]+',' ',line).strip() + '\n'
                file_b64 = base64.b64encode(str.encode(label_text))
                attachment_values = {
                    "name": "Label: {}".format(picking.name),
                    "type": "binary",
                    "datas": file_b64,
                    "datas_fname": "Label" + picking.name + ".txt",
                    "store_fname": picking.name,
                    "res_model": picking._name,
                    "res_id": picking.id,
                    "mimetype": "text/plain",
                }
            attachment = self.env["ir.attachment"].create(attachment_values)
            body = _("Nacex label for tracking ref {}").format(ncx_tracking_ref)
            picking.message_post(body=body, attachments=attachment)
        elif label and label[0] == "ERROR":
            _logger.error(
                _("Error while trying to retrieve the label: {}").format(
                    label[1]
                )
            )
            msg = _("Error while trying to retrieve the label with the ref {}: {}").format(ncx_tracking_ref, label)
            picking.message_post(body=msg)
            picking.failed_shipping = True
        else:
            _logger.error(
                _("Error while trying to retrieve the label")
            )
            picking.failed_shipping = True

    def ncx_cancel_shipment(self, pickings):
        for picking in pickings.filtered("carrier_tracking_ref"):
            ncx_request = NcxRequest(self)
            response = ncx_request.cancelExpedicion(picking.carrier_tracking_ref)
            self._ncx_check_cancel_response(response, picking)
            self._ncx_log_request(ncx_request)
        return True

    def ncx_tracking_state_update(self, picking):
        """Tracking state update"""
        self.ensure_one()
        if not picking.carrier_tracking_ref:
            return
        ncx_request = NcxRequest(self)
        res = ncx_request.getEstadoExpedicion(picking.carrier_tracking_ref)
        if res and res[0] != "ERROR":
            if res[4] and res[4] == 'OK':
                picking.delivered = True
                msg = _("Expedition with number %s has been delivered.") % (picking.carrier_tracking_ref)
                picking.message_post(body=msg)
                return
        elif res and res[0] == "ERROR":
            _logger.error(_("Error: {}").format(res[1]))
            return
        else:
            _logger.error(_("Error: after requesting shipment status"))
            return
