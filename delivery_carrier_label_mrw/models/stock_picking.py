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

from datetime import datetime

from requests import Session

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from zeep import Client
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport

_logger = logging.getLogger(__name__)

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipment_reference = fields.Char("Shipment Reference")
    failed_shipping = fields.Boolean("Failed Shipping", default=False)
    carrier_type = fields.Selection(related="carrier_id.carrier_type")
    delivery_note = fields.Char(compute="_compute_delivery_note")

    def print_created_labels(self):
        if self.carrier_type == "mrw":
            return self.print_mrw_label()
        return super(StockPicking, self).print_created_labels()

    def print_mrw_label(self):
        self.ensure_one()

        if not self.carrier_id.account_id.printer:
            return
        labels = self.env["ir.attachment"].search(
            [("res_id", "=", self.id), ("res_model", "=", self._name)]
        )
        for label in labels:
            if label.mimetype == "application/x-pdf":
                doc_format = "pdf"
            else:
                doc_format = "raw"
            self.carrier_id.account_id.printer.print_document(
                None, base64.b64decode(label.datas), doc_format=doc_format
            )

    def action_generate_carrier_label(self):
        if self.carrier_type == "mrw":
            return self._generate_mrw_label()
        return super().action_generate_carrier_label()
    
    @api.multi
    def remove_tracking_info(self):
        for pick in self.filtered(lambda x: x.carrier_type == "mrw"):
            pick.update({"shipment_reference": False})

            if pick.carrier_tracking_ref:
                client, history = pick.create_client()

                if client:

                    try:
                        headers = pick.setMRWHeaders(client)
                        res = pick.cancel_mrw_expedition(client, headers, pick.carrier_tracking_ref)

                        if res:
                            if res["Estado"] == "0":
                                raise AccessError(_("Error message: {}").format(res["Mensaje"]))
                            if res["Estado"] == "1":
                                msg = _("Expedition with number %s cancelled: %s") % (pick.carrier_tracking_ref, res["Mensaje"])
                            pick.message_post(body=msg)
                    except Exception as e:
                        raise AccessError(_("Access error message: {}").format(e))

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
            
    def create_tracking_client(self):
        session = Session()
        session.verify = False

        try:
            transport = Transport(cache=SqliteCache(), session=session)
            history = HistoryPlugin()
            if self.carrier_id.account_id.test_enviroment:
                url = self.carrier_id.account_id.mrw_tracking_service_test_url
            else:
                url = self.carrier_id.account_id.mrw_tracking_service_url
            client = Client(url, transport=transport, plugins=[history])

            if client:
                return client, history
            else:
                raise AccessError(_("Not possible to establish a client."))
        except Exception as e:
            raise AccessError(_("Access error message: {}".format(e)))

    def create_client(self):
        session = Session()
        session.verify = False

        try:
            transport = Transport(cache=SqliteCache(), session=session)
            history = HistoryPlugin()
            if self.carrier_id.account_id.test_enviroment:
                url = "http://sagec-test.mrw.es/MRWEnvio.asmx?WSDL"
            else:
                url = "http://sagec.mrw.es/MRWEnvio.asmx?WSDL"
            client = Client(url, transport=transport, plugins=[history])

            if client:
                return client, history
            else:
                raise AccessError(_("Not possible to establish a client."))
        except Exception as e:
            raise AccessError(_("Access error message: {}".format(e)))

    def setMRWHeaders(self, client):

        try:
            element_type = client.get_element("{http://www.mrw.es/}AuthInfo")            
            headers = element_type(
                CodigoFranquicia=self.carrier_id.account_id.mrw_franchise,
                CodigoAbonado=self.carrier_id.account_id.mrw_account,
                CodigoDepartamento="",
                UserName=self.carrier_id.account_id.account,
                Password=self.carrier_id.account_id.password,
            )
            return headers
        except Exception:
            return False

    def get_carrier_label(self, client, headers, numeroEnvio):
        EtiquetaEnvio = {
            "request": {
                "NumeroEnvio": numeroEnvio,
                "SeparadorNumerosEnvio": "",
                "ReportTopMargin": 1100,
                "ReportLeftMargin": 650,
            }
        }

        label = client.service.EtiquetaEnvio(**EtiquetaEnvio, _soapheaders=[headers])
        return label

    def _generate_mrw_label(self):
        if self.carrier_tracking_ref:
            return self.print_mrw_label()
        self.check_delivery_address()

        if not self.carrier_service:
            raise UserError("Carrier service not selected.")
        if not self.carrier_id.account_id:
            raise UserError("Delivery carrier has no account.")

        client, history = self.create_client()

        if client:

            try:
                headers = self.setMRWHeaders(client)

                notices = []
                if self.carrier_id.account_id.mrw_phone_notification:
                    phone_notification = {
                        "NotificacionRequest": {
                            "CanalNotificacion": "2",
                            "TipoNotificacion": self.carrier_id.account_id.mrw_notice_type,
                            "MailSMS": self.partner_id.phone
                            or self.partner_id.mobile
                            or self.partner_id.commercial_partner_id.phone
                            or self.partner_id.commercial_partner_id.mobile,
                        }
                    }
                    notices.append(phone_notification)

                if self.carrier_id.account_id.mrw_mail_notification:
                    mail_notification = {
                        "NotificacionRequest": {
                            "CanalNotificacion": "1",
                            "TipoNotificacion": self.carrier_id.account_id.mrw_notice_type,
                            "MailSMS": self.partner_id.email
                            or self.partner_id.commercial_partner_id.email,
                        }
                    }
                    notices.append(mail_notification)

                TransmEnvio = {
                    "request": {
                        "DatosEntrega": {
                            "Direccion": {
                                "Via": "{} {}".format(
                                    self.partner_id.street or "",
                                    self.partner_id.street2 or "",
                                ),
                                "CodigoPostal": self.partner_id.zip.replace(
                                    " ", ""
                                )[:4]
                                if self.partner_id.country_id.code == "PT"
                                else self.partner_id.zip.zfill(5)
                                if self.partner_id.country_id.code == "AD"
                                else self.partner_id.zip,
                                "Poblacion": self.partner_id.city,
                                "Provincia": self.partner_id.state_id.name,
                            },
                            "Nif": self.partner_id.vat,
                            "Nombre": self.partner_id.name,
                            "Telefono": self.partner_id.phone
                            or self.partner_id.mobile
                            or self.partner_id.commercial_partner_id.phone
                            or self.partner_id.commercial_partner_id.mobile
                            or "",
                            "Observaciones": "{}".format(self.delivery_note),
                        },
                        "DatosServicio": {
                            "Fecha": datetime.now().strftime(
                                "%d/%m/%Y"
                            ),  # self.date.strftime("%d/%m/%Y"),
                            "Referencia": self.name,
                            "CodigoServicio": self.carrier_service.carrier_code,
                            "Frecuencia": self.carrier_id.account_id.mrw_frequency
                            if self.carrier_service.carrier_code == "0005"
                            else "",
                            "NumeroBultos": self.carrier_packages,
                            "Peso": round(self.carrier_weight),
                            "EntregaSabado": self.carrier_id.account_id.mrw_saturday_delivery,
                            "Entrega830": self.carrier_id.account_id.mrw_830_delivery,
                            "Gestion": self.carrier_id.account_id.mrw_delivery_hangle,
                            "ConfirmacionInmediata": self.carrier_id.account_id.mrw_instant_notice,
                            "Reembolso": self.carrier_id.account_id.mrw_delivery_pdo
                            if self.payment_on_delivery
                            else "N",
                            "ImporteReembolso": "{}".format(self.pdo_quantity).replace(".", ",")
                            if self.carrier_id.account_id.mrw_delivery_pdo != "N"
                            and self.payment_on_delivery
                            else "",
                            "TipoMercancia": self.carrier_id.account_id.mrw_goods_type
                            if self.partner_id.country_id.code != "ES"
                            else "",
                            "Notificaciones": notices,
                        },
                    }
                }

                res = client.service.TransmEnvio(
                    **TransmEnvio, _soapheaders=[headers]
                )
            except Exception as e:
                self.failed_shipping = True
                raise AccessError(_("Access error message: {}").format(e))

            if res["Estado"] == "0":
                self.failed_shipping = True
                raise AccessError(_("Error message: {}").format(res["Mensaje"]))
            elif res["Estado"] == "1":

                self.write(
                    {
                        "carrier_tracking_ref": res["NumeroEnvio"],
                        "shipment_reference": res["NumeroSolicitud"],
                    }
                )

                try:
                    label = self.get_carrier_label(
                        client, headers, res["NumeroEnvio"]
                    )
                except Exception as e:
                    _logger.error(
                        _(
                            "Connection error: {}, while trying to retrieve the label."
                        ).format(e)
                    )
                    self.failed_shipping = True
                    return

                if label["Estado"] == "1":
                    file_b64 = base64.b64encode(label["EtiquetaFile"])
                    self.env["ir.attachment"].create(
                        {
                            "name": "Label: {}".format(self.name),
                            "type": "binary",
                            "datas": file_b64,
                            "datas_fname": "Label" + self.name + ".pdf",
                            "store_fname": self.name,
                            "res_model": self._name,
                            "res_id": self.id,
                            "mimetype": "application/x-pdf",
                        }
                    )
                    self.failed_shipping = False
                elif label["Estado"] == "0":
                    raise AccessError(
                        _("Error while trying to retrieve the label: {}").format(
                            label["Mensaje"]
                        )
                    )
                    self.failed_shipping = True
                else:
                    self.failed_shipping = True
                    raise AccessError(_("Error while trying to retrieve the label"))
            else:
                self.failed_shipping = True
                raise AccessError(_("Unknown error with the SOAP connection."))

        else:
            self.failed_shipping = True
            raise AccessError(_("Not possible to establish a client."))

        self.print_mrw_label()

        if self.payment_on_delivery:
            self.mark_as_paid_shipping()

    def get_state_id(self, partner_id):
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

    def check_delivery_address(self):
        if self.carrier_type == "mrw":   
            if not self.partner_id.state_id:
                state_id = self.get_state_id(self.partner_id)
                if not state_id:
                    raise UserError(
                        _("Partner address is not complete (State missing).")
                    )
                else:
                    self.partner_id.state_id = state_id["state_id"]

    def check_shipment_status(self):
        if self.carrier_type == "mrw":
            if not self.carrier_id.account_id:
                _logger.error(_("Delivery carrier has no account."))
                return

            client, history = self.create_tracking_client()

            if not client:
                _logger.error(_("Not possible to establish a client."))
                return

            try:
                GetEnvios = {
                    "login": self.carrier_id.account_id.mrw_tracking_user,
                    "pass": self.carrier_id.account_id.mrw_tracking_password,
                    "codigoIdioma": 3082,
                    "tipoFiltro": 0,
                    "valorFiltroDesde": self.carrier_tracking_ref,
                    "tipoInformacion": 1,
                    "codigoAbonado": self.carrier_id.account_id.mrw_account,
                    "codigoFranquicia": self.carrier_id.account_id.mrw_franchise,
                }

                res = client.service.GetEnvios(**GetEnvios)
            except Exception as e:
                _logger.error(_("Access error message: {}").format(e))
                return
            if (
                res["Seguimiento"]["Abonado"]
                and "SeguimientoAbonado" in res["Seguimiento"]["Abonado"][0]
            ):
                for seguimiento in res["Seguimiento"]["Abonado"][0][
                    "SeguimientoAbonado"
                ]["Seguimiento"]:
                    if seguimiento["Estado"] == "00":
                        self.delivered = True
                        break

            else:
                _logger.error(_("Error: {}").format(res["MensajeSeguimiento"]))
                return

    def cancel_mrw_expedition(self, client, headers, NumeroEnvioOriginal):
        CancelarEnvio = {
            "request": {
                "CancelaEnvio": {
                    "NumeroEnvioOriginal": NumeroEnvioOriginal,
                }
            }
        }

        response = client.service.CancelarEnvio(**CancelarEnvio, _soapheaders=[headers])
        return response