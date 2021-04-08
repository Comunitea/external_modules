##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2020 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See thefire
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
import base64
import re

from datetime import datetime

from requests import Session

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.addons import decimal_precision as dp
from zeep import Client
from zeep import xsd
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport

import urllib.request

_logger = logging.getLogger(__name__)

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging.config

""" logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
           'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
       },
   }
}) """


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipment_reference = fields.Char("Shipment Reference")
    failed_shipping = fields.Boolean("Failed Shipping", default=False)
    carrier_type = fields.Selection(related="carrier_id.carrier_type")
    delivery_note = fields.Char(compute="_compute_delivery_note")
    ncx_shipping_return = fields.Boolean("Shipping with return", default=False)

    def create_client_ncx(self):
        session = Session()
        session.verify = False

        try:
            transport = Transport(cache=SqliteCache(), session=session)
            history = HistoryPlugin()
            url = "http://pda.nacex.com/nacex_ws/soap?wsdl"
            client = Client(url, transport=transport, plugins=[history])

            if client:
                return client, history
            else:
                raise AccessError(_("Not possible to establish a client."))
        except Exception as e:
            raise AccessError(_("Access error message: {}".format(e)))

    def print_created_labels(self):
        if self.carrier_type == "ncx":
            return self.print_ncx_label()
        return super(StockPicking, self).button_validate()

    def print_ncx_label(self):
        self.ensure_one()

        if not self.carrier_id.account_id.printer:
            return
        labels = self.env["ir.attachment"].search(
            [("res_id", "=", self.id), ("res_model", "=", self._name)]
        )
        for label in labels:
            if label.mimetype == "image/png":
                doc_format = "png"
            else:
                doc_format = "raw"
            self.carrier_id.account_id.printer.print_document(
                None, base64.b64decode(label.datas), doc_format=doc_format
            )

    def action_generate_carrier_label(self):
        if self.carrier_type == "ncx":
            return self._generate_ncx_label()
        return super().action_generate_carrier_label()

    @api.multi
    def remove_tracking_info(self):
        for pick in self.filtered(lambda x: x.carrier_type == "ncx"):
            pick.update({"shipment_reference": False})

            if pick.carrier_tracking_ref:
                self.remove_tracking_ncx()

        return super().remove_tracking_info()

    @api.depends("sale_id")
    def _compute_delivery_note(self):
        for pick in self:
            delivery_note = ""
            if pick and pick.sale_id:
                delivery_note += "{} ".format(pick.sale_id.note)
            if delivery_note.strip() == "":
                delivery_note = "N/A"
            pick.delivery_note = delivery_note[:45]

    def shipment_status_ncx(self):
        client, history = self.create_client_ncx()

        if client:

            getEstadoExpedicion = {
                "String_1": self.carrier_id.account_id.account,
                "String_2": self.carrier_id.account_id.password,
                "String_3": self.carrier_tracking_ref,
            }

            with client.settings(strict=False):

                service = client.create_service(
                    '{urn:soap/types}nacexwsImplServiceSoapBinding',
                    'http://pda.nacex.com/nacex_ws/soap')

                res = service.getEstadoExpedicion(**getEstadoExpedicion)
            if res and res[0] != "ERROR":
                if res[4] and res[4] == 'OK':
                    self.delivered = True
                    msg = _("Expedition with number %s has been delivered.") % (self.carrier_tracking_ref)
                    self.message_post(body=msg)
                    return
            elif res and res[0] == "ERROR":
                _logger.error(_("Error: {}").format(res[1]))
                return
            else:
                _logger.error(_("Error: after requesting shipment status"))
                return

    def remove_tracking_ncx(self):
        client, history = self.create_client_ncx()

        if client:
            
            arrayOfString_3 = [
                "expe_codigo={}".format(self.carrier_tracking_ref),  
            ]

            cancelExpedicion = {
                "String_1": self.carrier_id.account_id.account,
                "String_2": self.carrier_id.account_id.password,
                "arrayOfString_3": arrayOfString_3
            }

            with client.settings(strict=False):

                service = client.create_service(
                    '{urn:soap/types}nacexwsImplServiceSoapBinding',
                    'http://pda.nacex.com/nacex_ws/soap')

                res = service.cancelExpedicion(**cancelExpedicion)
            if res and res._raw_elements and res._raw_elements[0].text == 'ERROR':
                msg = _("Access error message: {}").format(res._raw_elements[0].text)
                raise AccessError(msg)
            elif res and res._raw_elements and res._raw_elements[0].text:
                msg = _("Expedition with number %s cancelled: %s") % (self.carrier_tracking_ref, res._raw_elements[0].text)
                self.message_post(body=msg)
            else:
                msg = _("Access error")
                raise AccessError(msg)
                    
    def get_ncx_label(self, client, numeroEnvio):

        getEtiqueta = {
            "String_1": self.carrier_id.account_id.account,
            "String_2": self.carrier_id.account_id.password,
            "String_3": numeroEnvio,
            "String_4": self.carrier_id.account_id.ncx_printer_model
        }

        with client.settings(strict=False):

            service = client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                'http://pda.nacex.com/nacex_ws/soap')

            label = service.getEtiqueta(**getEtiqueta)
            return label

    def _generate_ncx_label(self):
        if self.carrier_tracking_ref:
            return self.print_ncx_label()
        self.check_delivery_address()

        if not self.carrier_service:
            raise UserError("Carrier service not selected.")
        if not self.carrier_id.account_id:
            raise UserError("Delivery carrier has no account.")

        client, history = self.create_client_ncx()

        if client:

            arrayOfString_3 = [
                "del_cli={}".format(self.carrier_id.account_id.ncx_delegation),
                "num_cli={}".format(self.carrier_id.account_id.ncx_client),
                "tip_ser={}".format(self.carrier_service.carrier_code),
                "tip_cob={}".format(self.carrier_id.account_id.ncx_payment_type),
                "ref_cli={}".format(self.name),
                "tip_env={}".format(self.carrier_id.account_id.ncx_package_type),
                "bul={}".format(self.carrier_packages),
                "kil={}".format(round(self.carrier_weight)),
                "nom_ent={}".format(self.partner_id.display_name[:50]),
                "dir_ent={} {}".format(self.partner_id.street if self.partner_id.street else '', self.partner_id.street2 if self.partner_id.street2 else ''),
                "pais_ent={}".format(self.partner_id.country_id.code),
                "cp_ent={}".format(self.partner_id.zip),
                "pob_ent={}".format(self.partner_id.city),
                "tel_ent={}".format(self.partner_id.phone if self.partner_id.phone else self.partner_id.mobile if self.partner_id.mobile else ''),
                "obs1={}".format(self.delivery_note[0:38] if self.delivery_note else ''),
                "obs2={}".format(self.delivery_note[38:75] if self.delivery_note else ''),
                "obs3={}".format(self.delivery_note[75:113] if self.delivery_note else ''),
                "obs4={}".format(self.delivery_note[113:151] if self.delivery_note else ''),
                "ret={}".format("S" if self.ncx_shipping_return else "N"),
                "ree={}".format(self.pdo_quantity),
                "tip_ree={}".format(self.carrier_id.account_id.ncx_pod_type if self.payment_on_delivery else 'N'),   
            ]

            putExpedicion = {
                "String_1": self.carrier_id.account_id.account,
                "String_2": self.carrier_id.account_id.password,
                "arrayOfString_3": arrayOfString_3
            }

            try:
                _logger.info("putExpedicion: {}".format(putExpedicion))
                with client.settings(strict=False):

                    service = client.create_service(
                        '{urn:soap/types}nacexwsImplServiceSoapBinding',
                        'http://pda.nacex.com/nacex_ws/soap')

                    res = service.putExpedicion(
                        **putExpedicion
                    )
            except Exception as e:
                try:
                    msg = _("Access error message: {}").format(history.last_received['envelope'][0][0][1].text)
                except:
                    msg = _("Access error message: {}").format(e)
                self.failed_shipping = True
                raise AccessError(msg)

        if res and res._raw_elements and res._raw_elements[0].text =='ERROR':
            raise AccessError(_("Error message: {}").format(res._raw_elements[1].text))
        elif res:

            self.write(
                {
                    "carrier_tracking_ref": res._raw_elements[0].text,
                    "shipment_reference": res._raw_elements[1].text,
                }
            )

            try:
                label = self.get_ncx_label(client, res._raw_elements[0].text)
                _logger.debug("label: {}".format(label))
            except Exception as e:
                try:
                    _logger.error(
                        _(
                            "Connection error: {}, while trying to retrieve the label."
                        ).format(history.last_received['envelope'][0][0][1].text)
                    )
                except:
                    msg = _("Access error message: {}").format(e)
                    _logger.error(
                        _(
                            "Connection error: {}, while trying to retrieve the label."
                        ).format(e)
                    )
                self.failed_shipping = True
                return

            try:
                if label and label[0] != "ERROR":
                    if self.carrier_id.account_id.ncx_printer_model == "IMAGEN_B":
                        file_b64 = self.base64_url_decode(label)

                        attachment_values = {
                            "name": "Label: {}".format(self.name),
                            "type": "binary",
                            "datas": base64.b64encode(file_b64),
                            "datas_fname": "Label" + self.name + ".png",
                            "store_fname": self.name,
                            "res_model": self._name,
                            "res_id": self.id,
                            "mimetype": "image/png",
                        }

                    else:
                        # We need to replace blank spaces with line breaks
                        label_text = ''
                        for line in label:
                            label_text += re.sub('[^!-~]+',' ',line).strip() + '\n'
                        file_b64 = base64.b64encode(str.encode(label_text))
                        attachment_values = {
                            "name": "Label: {}".format(self.name),
                            "type": "binary",
                            "datas": file_b64,
                            "datas_fname": "Label" + self.name + ".txt",
                            "store_fname": self.name,
                            "res_model": self._name,
                            "res_id": self.id,
                            "mimetype": "text/plain",
                        }
                    self.env["ir.attachment"].create(attachment_values)
                elif label and label[0] == "ERROR":
                    _logger.error(
                        _("Error while trying to retrieve the label: {}").format(
                            label[1]
                        )
                    )
                    self.failed_shipping = True
                else:
                    _logger.error(
                        _("Error while trying to retrieve the label")
                    )
                    self.failed_shipping = True
            except Exception as e:
                _logger.error(
                    _(
                        "Connection error: {}, while trying to save the label."
                    ).format(e)
                )
                self.failed_shipping = True
                return
        else:
            raise UserError(
                _("There was an error connecting to Nacex. Check the connection log.")
            )
            self.failed_shipping = True

        self.failed_shipping = False
        self.print_ncx_label()

        if self.payment_on_delivery:
            self.mark_as_paid_shipping()

    def check_delivery_address(self):
        if self.carrier_type == "ncx":
            if not self.partner_id.state_id:
                state_id = self.get_state_id(self.partner_id)
                if not state_id:
                    raise UserError(
                        _("Partner address is not complete (State missing).")
                    )
                else:
                    self.partner_id.state_id = state_id["state_id"]

    def check_shipment_status(self):
        if self.carrier_type == "ncx":
            if not self.carrier_id.account_id:
                _logger.error(_("Delivery carrier has no account."))
                return

            self.shipment_status_ncx()

    def base64_url_decode(self, label):
        padding_factor = (4 - len(label) % 4) % 4
        label += "="*padding_factor
        return base64.b64decode(str(label).translate(dict(zip(map(ord, u'-_'), u'+/'))))
