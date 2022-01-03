##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
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
import logging
import base64
import re

from odoo import models, fields, _
from odoo.exceptions import UserError

from .nacex_request import (
    NACEX_PRINTER_MODEL,
    NACEX_PAYMENT_TYPE,
    NACEX_PACKAGE_TYPE,
    NACEX_POD_TYPE,
    NACEX_SERVICE_CODE,
    NacexRequest,
)

_logger = logging.getLogger(__name__)

class DeliveryCarrier(models.Model):

    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(
        selection_add=[("nacex", "NACEX")],
        ondelete="set default",
    )
    ncx_account = fields.Char(string="Nacex Account Number", required=True)
    ncx_password = fields.Char(string="Nacex Account Password", required=True)
    ncx_client = fields.Char("NACEX Client Code")
    ncx_delegation = fields.Char("NACEX Delegation Code")
    ncx_client_department = fields.Char("NACEX Franchise Code")
    ncx_oldmodel = fields.Boolean(string='Old model', help="Old models can't print more than 64 characters.")
    ncx_shipping_return = fields.Boolean("Shipping with return", default=False)
    ncx_service_code = fields.Selection(
        string="Nacex service code",
        selection=NACEX_SERVICE_CODE,
        default="01",
    )
    ncx_printer_model = fields.Selection(
        string="Nacex printer model",
        selection=NACEX_PRINTER_MODEL,
        default="TECSV4_B",
    )
    ncx_payment_type = fields.Selection(
        string="Nacex payment type",
        selection=NACEX_PAYMENT_TYPE,
        default="O",
    )
    ncx_package_type = fields.Selection(
        string="Nacex package type",
        selection=NACEX_PACKAGE_TYPE,
        default="2",
    )
    ncx_pod_type = fields.Selection(
        string="Nacex payment on delivery type",
        selection=NACEX_POD_TYPE,
        default="D",
    )

    def nacex_send_shipping(self, pickings):
        return [self.nacex_create_shipping(p) for p in pickings]

    def nacex_get_tracking_link(self, picking):
        return "http://www.nacex.es/irSeguimiento.do?seguimiento={}".format(
            picking.carrier_tracking_ref
        )
    
    def get_nacex_state_id(self, partner_id):
        if partner_id.country_id and partner_id.zip:
            city_zip = self.env["res.city.zip"].search(
                [
                    ("name", "=", partner_id.zip),
                    ("city_id.country_id", "=", partner_id.country_id.id),
                ],
                limit=1,
            )
            if not city_zip:
                # Portugal
                city_zip = self.env["res.city.zip"].search(
                    [
                        ("name", "=", partner_id.zip.replace(" ", "-")),
                        ("city_id.country_id", "=", partner_id.country_id.id),
                    ],
                    limit=1,
                )
                if not city_zip:
                    # Portugal 2
                    city_zip = self.env["res.city.zip"].search(
                        [
                            (
                                "name",
                                "=",
                                partner_id.zip[:4] + "-" + partner_id.zip[4:],
                            ),
                            ("city_id.country_id", "=", partner_id.country_id.id),
                        ],
                        limit=1,
                    )
            if city_zip:
                return {"state_id": city_zip.city_id.state_id.id}
    
    def nacex_check_delivery_address(self, picking):
        if not picking.partner_id.state_id:
            state_id = self.get_nacex_state_id(picking.partner_id)
            if not state_id:
                raise UserError(
                    _("Partner address is not complete (State missing).")
                )
            else:
                picking.partner_id.state_id = state_id["state_id"]
    
    def nacex_base64_url_decode(self, label):
        padding_factor = (4 - len(label) % 4) % 4
        label += "="*padding_factor
        return base64.b64decode(str(label).translate(dict(zip(map(ord, u'-_'), u'+/'))))
    
    def _prepare_nacex_shipping(self, picking):
        arrayOfString_3 = [
            "del_cli={}".format(self.ncx_delegation),
            "num_cli={}".format(self.ncx_client),
            "tip_ser={}".format(self.ncx_service_code),
            "tip_cob={}".format(self.ncx_payment_type),
            "ref_cli={}".format(picking.name),
            "tip_env={}".format(self.ncx_package_type),
            "bul={}".format(picking.number_of_packages or 1),
            "kil={}".format(round(picking.shipping_weight)),
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

        if picking.ncx_payment_on_delivery and self.ncx_pod_type:
            arrayOfString_3.append("ree={}".format(picking.ncx_pdo_quantity))
            arrayOfString_3.append("tip_ree={}".format(self.ncx_pod_type))

        putExpedicion = {
            "String_1": self.ncx_account,
            "String_2": self.ncx_password,
            "arrayOfString_3": arrayOfString_3
        }

        return putExpedicion
    
    def nacex_get_label(self, carrier_tracking_ref):
        self.ensure_one()
        nacex_request = NacexRequest(self)

        getEtiqueta = {
            "String_1": self.ncx_account,
            "String_2": self.ncx_password,
            "String_3": carrier_tracking_ref,
            "String_4": self.ncx_printer_model
        }

        label = nacex_request.print_shipment(getEtiqueta)

        return label or False, nacex_request
    
    def nacex_save_label(self, picking):
        self.ensure_one()
        if not picking.carrier_tracking_ref:
            return False
        try:
            label, nacex_request = self.nacex_get_label(picking.carrier_tracking_ref)
            _logger.debug("label: {}".format(label))
        except Exception as e:
            try:
                picking.message_post(
                    body=_("Connection error: {}, while trying to retrieve the label.").format(nacex_request.history.last_received['envelope'][0][0][1].text)
                )
            except:
                picking.message_post(
                    body=_("Connection error: {}, while trying to retrieve the label.").format(e)
                )
            return

        try:
            if label and label[0] != "ERROR":
                if self.ncx_printer_model == "IMAGEN_B":
                    file_b64 = self.nacex_base64_url_decode(label)

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
                self.env["ir.attachment"].create(attachment_values)
            elif label and label[0] == "ERROR":
                picking.message_post(
                    body=_("Error while trying to retrieve the label: {}").format(label[1])
                )
            else:
                picking.message_post(
                    body=_("Error while trying to retrieve the label")
                )
        except Exception as e:
            _logger.error(
                _(
                    "Connection error: {}, while trying to save the label."
                ).format(e)
            )
            picking.message_post(
                body=_("Connection error: {}, while trying to save the label.").format(e)
            )
    
    def nacex_create_shipping(self, pickings):
        nacex_request = NacexRequest(self)

        result = []
        for picking in pickings:
            try:
                self.nacex_check_delivery_address(picking)
            except Exception as e:
                picking.message_post(body=_("Impossible to retrieve the label: {}".format(e)))
                result.append(False)
                continue       

            if not self.ncx_service_code:
                picking.message_post(body=_("Carrier service not selected."))
                result.append(False)
                continue
            if not self.carrier_id.ncx_account:
                picking.message_post(body=_("Delivery carrier has no account."))
                result.append(False)
                continue

            
            vals = self._prepare_nacex_shipping(picking)

            try:
                _logger.info("putExpedicion: {}".format(vals))
                response = nacex_request.create_shipment(vals)
            except Exception as e:
                try:
                    msg = _("Access error message: {}").format(nacex_request.history.last_received['envelope'][0][0][1].text)
                except:
                    msg = _("Access error message: {}").format(e)
                picking.message_post(body=msg)
                result.append(False)
                continue

            if response and response._raw_elements and response._raw_elements[0].text =='ERROR':
                picking.message_post(body=_("Error message: {}").format(response._raw_elements[1].text))
                result.append(False)
                continue
            elif response:
                vals = {
                    "carrier_tracking_ref": response._raw_elements[0].text,
                    "shipment_reference": response._raw_elements[1].text,
                }
                result.append(vals)
                self.nacex_save_label(picking)
            else:
                picking.message_post(
                    body=_("There was an error connecting to Nacex. Check the connection log.")
                )
                result.append(False)
                continue
        return result
    
    def nacex_cancel_shipment(self, pickings):
        nacex_request = NacexRequest(self)
        for picking in pickings.filtered("carrier_tracking_ref"):

            arrayOfString_3 = [
                "expe_codigo={}".format(self.carrier_tracking_ref),  
            ]

            cancelExpedicion = {
                "String_1": self.ncx_account,
                "String_2": self.ncx_password,
                "arrayOfString_3": arrayOfString_3
            }

            res = nacex_request.cancel_shipment(cancelExpedicion)
            msg = False

            if res and res._raw_elements and res._raw_elements[0].text == 'ERROR':
                msg = _("Access error message: {}").format(res._raw_elements[0].text)
            elif res and res._raw_elements and res._raw_elements[0].text:
                msg = _("Expedition with number %s cancelled: %s") % (self.carrier_tracking_ref, res._raw_elements[0].text)
                picking.update({
                    "shipment_reference": False,
                    "carrier_tracking_ref": False
                })
            else:
                msg = _("Access error")
            picking.message_post(body=msg)
        return True
    
    def nacex_tracking_state_update(self, picking):
        self.ensure_one()
        nacex_request = NacexRequest(self)
        
        if (
            picking.carrier_tracking_ref
        ):
            getEstadoExpedicion = {
                "String_1": self.ncx_account,
                "String_2": self.ncx_password,
                "String_3": picking.carrier_tracking_ref,
            }

            res = nacex_request.track_shipment(getEstadoExpedicion)
            msg = False

            if res and res[0] != "ERROR":
                if res[4] and res[4] == 'OK':
                    msg = _("Expedition with number %s has been delivered.") % (picking.carrier_tracking_ref)
            elif res and res[0] == "ERROR":
                msg = _("Error: {}").format(res[1])
            else:
                msg = _("Error: after requesting shipment status")

            picking.message_post(body=msg)
            return
