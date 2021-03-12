# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
import os
import re
from base64 import b64decode, b64encode
from datetime import date
from xml.dom.minidom import parseString

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from unidecode import unidecode

try:
    import genshi
    import genshi.template
except (ImportError, IOError) as err:
    import logging

    logging.getLogger(__name__).warn("Module genshi is not available")

loader = genshi.template.TemplateLoader(
    os.path.join(os.path.dirname(__file__), "template"), auto_reload=True
)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def _generate_cex_label(self, package_ids=None):
        self.ensure_one()

        url = (
            self.carrier_id.account_id.test_enviroment
            and "https://test.correosexpress.com/wspsc/apiRestGrabacionEnvio"
            "/json/grabacionEnvio"
            or "https://www.correosexpress.com/wpsc/apiRestGrabacionEnvio/"
            "json/grabacionEnvio"
        )
        username = self.carrier_id.account_id.account
        password = self.carrier_id.account_id.password
        data = self._get_cex_label_data()
        try:
            response = requests.post(
                url, auth=(username, password), json=data, timeout=5
            )
            rjson = json.loads(re.search("({.*})", response.text).group(1))
        except requests.exceptions.Timeout:
            rjson = {
                "codigoRetorno": 999,
                "mensajeRetorno": "\n\nEl servidor está tardando mucho en responder.",
            }
        except:
            rjson = {"codigoRetorno": 999, "mensajeRetorno": "\n\n" + response.text}
        retorno = rjson["codigoRetorno"]
        message = rjson["mensajeRetorno"]

        if retorno == 0:
            self.carrier_tracking_ref = rjson["datosResultado"]
            if self.carrier_id.account_id.file_format == "PDF":
                if self.payment_on_delivery:
                    self.mark_as_paid_shipping()
                self.failed_shipping = False
                return [
                    {
                        "name": "Label: {}".format(self.name),
                        "file": b64decode(label_result["etiqueta1"]),
                        "file_type": "pdf",
                    }
                    for label_result in rjson["etiqueta"]
                ]
            else:
                self.cex_result = rjson["etiqueta"][0]["etiqueta2"]
                if self.payment_on_delivery:
                    self.mark_as_paid_shipping()
                self.failed_shipping = False
                return [
                    {
                        "name": "Label: {}.txt".format(self.name),
                        "file": b64encode(label_result["etiqueta2"].encode("utf-8")),
                        "file_type": "txt",
                    }
                    for label_result in rjson["etiqueta"]
                ]
        else:
            raise UserError(
                _("CEX Error: %s %s") % (retorno or 999, message or "Webservice ERROR.")
            )
            self.failed_shipping = True

        return False

    @api.multi
    def number_of_packages_for_cex(self):
        self.ensure_one()
        # TODO check pack operation no disponible en v 12
        if self.has_packages:
            return len(self.move_line_ids.filtered(lambda ml: ml.result_package_id))

    def _get_cex_label_data(self):
        self.ensure_one()

        partner = self.partner_id
        number_of_packages = self.carrier_packages or 1
        phone = partner.mobile or partner.phone or ""
        listaBultos = []
        for i in range(0, number_of_packages):
            listaBultos.append(
                {
                    "ancho": "",
                    "observaciones": "",
                    "kilos": "",
                    "codBultoCli": "",
                    "codUnico": "",
                    "descripcion": "",
                    "alto": "",
                    "orden": i + 1,
                    "referencia": "",
                    "volumen": "",
                    "largo": "",
                }
            )

        streets = []
        if partner.street:
            streets.append(unidecode(partner.street))
        if partner.street2:
            streets.append(unidecode(partner.street2))
        if not streets or not partner.city or not partner.zip or not partner.zip or not partner.name:
            raise UserError("Review partner data")
        if self.carrier_id.account_id.file_format not in ("PDF", "ZPL"):
            raise UserError("Format file not supported by cex")
        if not self.carrier_service:
            raise UserError("Set service to the picking")
        if not self.carrier_weight or self.carrier_weight == 0.0:
            raise UserError("Set weight to the picking")
        data = {
            "solicitante": self.carrier_id.account_id.cex_solicitante,
            "canalEntrada": "",
            "numEnvio": "",
            "ref": self.origin[:20],
            "refCliente": "",
            "fecha": date.today().strftime("%d%m%Y"),
            "codRte": self.carrier_id.account_id.cex_codRte,
            "nomRte": self.company_id.name,
            "nifRte": "",
            "dirRte": self.company_id.street,
            "pobRte": self.company_id.city,
            "codPosNacRte": self.company_id.zip,
            "paisISORte": "",
            "codPosIntRte": "",
            "contacRte": self.company_id.name,
            "telefRte": self.company_id.phone,
            "emailRte": self.company_id.email,
            "codDest": "",
            "nomDest": partner.name[:40] or "",
            "nifDest": "",
            "dirDest": "".join(streets)[:300],
            "pobDest": partner.city[:50] or "",
            "codPosNacDest": partner.zip if partner.country_id.code == 'ES' else "",
            "paisISODest": "" if partner.country_id.code == 'ES' else partner.country_id.code,
            "codPosIntDest": "" if partner.country_id.code == 'ES' else partner.zip.replace(' ', ''),
            "contacDest": partner.name[:40] or "",
            "telefDest": phone[:15],
            "emailDest": partner.email and partner.email[:75] or "",
            "contacOtrs": "",
            "telefOtrs": "",
            "emailOtrs": "",
            "observac": "",
            "numBultos": number_of_packages or 1,
            "kilos": "%.3f" % (self.carrier_weight or 1),
            "volumen": "",
            "alto": "",
            "largo": "",
            "ancho": "",
            "producto": self.carrier_service.carrier_code,
            "portes": "P",
            "reembolso": "{}".format(self.pdo_quantity).replace(".", ",") if self.payment_on_delivery else "",
            "entrSabado": "",
            "seguro": "",
            "numEnvioVuelta": "",
            "listaBultos": listaBultos,
            "codDirecDestino": "",
            "password": "string",
            "listaInformacionAdicional": [
                {
                    "tipoEtiqueta": self.carrier_id.account_id.file_format == "PDF"
                    and "1"
                    or "2",
                    "etiquetaPDF": "",
                }
            ],
        }
        return data

    @api.multi
    def generate_cex_labels(self, package_ids=False):
        """ Generate the labels.
        A list of package ids can be given, in that case it will generate
        the labels only of these packages.
        """
        label_obj = self.env["shipping.label"]

        for pick in self:
            if package_ids:
                shipping_labels = pick._generate_cex_label(package_ids=package_ids)
            else:
                shipping_labels = pick._generate_cex_label()
            for label in shipping_labels:
                data = {
                    "name": label["name"],
                    "datas_fname": label.get("filename", label["name"]),
                    "res_id": pick.id,
                    "res_model": "stock.picking",
                    "datas": label["file"],
                    "file_type": label["file_type"],
                }
                if label.get("package_id"):
                    data["package_id"] = label["package_id"]
                context_attachment = self.env.context.copy()
                if self.carrier_id.account_id.printer:
                    self.carrier_id.account_id.printer.print_document(
                        None, b64decode(label["file"]), doc_format="raw"
                    )
                # remove default_type setted for stock_picking
                # as it would try to define default value of attachement
                if "default_type" in context_attachment:
                    del context_attachment["default_type"]
                label_obj.with_context(context_attachment).create(data)
        return True

    def action_generate_carrier_label(self):
        if self.carrier_id.carrier_type == "cex":
            number_of_packages = self.number_of_packages_for_cex()
            if number_of_packages:
                self.carrier_packages = number_of_packages
            return self.generate_cex_labels()
        return super().action_generate_carrier_label()

    def check_shipment_status(self):
        self.ensure_one()
        if self.carrier_id.carrier_type == "cex":
            url = "https://www.correosexpress.com/wpsc/apiRestSeguimientoEnvios/rest/seguimientoEnvios"
            username = self.carrier_id.account_id.account
            password = self.carrier_id.account_id.password
            vals = {
                "solicitante": self.carrier_id.account_id.cex_solicitante,
                "dato": self.carrier_tracking_ref,
            }
            tmpl = loader.load("check_status.xml")
            xml = tmpl.generate(**vals).render()
            try:
                response = requests.post(
                    url,
                    auth=(username, password),
                    data=xml,
                    timeout=5000,
                    headers={"Content-Type": "text/xml; charset=utf-8"},
                )
                xml_start = response.content.decode().find("<")
                result_xml = parseString(response.content.decode()[xml_start:])
                state_nodes = result_xml.getElementsByTagName("EstadoEnvios")
                for state_node in state_nodes:
                    if (
                        state_node.getElementsByTagName("CodEstado")
                        and state_node.getElementsByTagName("CodEstado")[
                            0
                        ].firstChild.data
                        == "12"
                    ):
                        self.delivered = True
                        break
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
                rjson = {
                    "codigoRetorno": 999,
                    "mensajeRetorno": "\n\nEl servidor está tardando mucho en responder.",
                }
            except:
                rjson = {"codigoRetorno": 999, "mensajeRetorno": "\n\n" + response.text}
        else:
            return super().check_shipment_status()
