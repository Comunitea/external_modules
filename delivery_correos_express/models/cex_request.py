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


class CexRequest:
    def __init__(self, carrier):        
        self.carrier = carrier
        self.api_env = "prod" if self.carrier.prod_environment else "test"

    
    def _generate_cex_label(self, picking):
        url = {
            "test": "https://test.correosexpress.com/wspsc/apiRestGrabacionEnvio/json/grabacionEnvio",
            "prod": "https://www.correosexpress.com/wpsc/apiRestGrabacionEnvio/json/grabacionEnvio",
        }
        url = url[self.api_env]
        username = self.cex_account
        password = self.cex_password       
        data = picking._prepare_cex_shipping() 
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
            picking.carrier_tracking_ref = rjson["datosResultado"]
            if self.carrier.file_format == "PDF":
                if self.carrier.cex_payment_on_delivery:
                    picking.mark_as_paid_shipping()
                picking.failed_shipping = False
                return [
                    {
                        "name": "Label: {}".format(picking.name),
                        "file": b64decode(label_result["etiqueta1"]),
                        "file_type": "pdf",
                    }
                    for label_result in rjson["etiqueta"]
                ]
            else:
                picking.cex_result = rjson["etiqueta"][0]["etiqueta2"]
                if self.carrier.payment_on_delivery:
                    picking.mark_as_paid_shipping()
                picking.failed_shipping = False
                return [
                    {
                        "name": "Label: {}.txt".format(picking.name),
                        "file": b64encode(label_result["etiqueta2"].encode("utf-8")),
                        "file_type": "txt",
                    }
                    for label_result in rjson["etiqueta"]
                ]
        else:
            raise UserError(
                _("CEX Error: %s %s") % (retorno or 999, message or "Webservice ERROR.")
            )
            picking.failed_shipping = True

        return False

    def check_shipment_status(self, picking):
        self.ensure_one()
        url = "https://www.correosexpress.com/wpsc/apiRestSeguimientoEnvios/rest/seguimientoEnvios"
        username = self.cex_account
        password = self.cex_password
        vals = {
            "solicitante": self.cex_solicitante,
            "dato": picking.carrier_tracking_ref,
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
                    picking.delivered = True
                    msg = _("Expedition with number %s has been delivered.") % (picking.carrier_tracking_ref)
                    picking.message_post(body=msg)
                    break
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
            rjson = {
                "codigoRetorno": 999,
                "mensajeRetorno": "\n\nEl servidor está tardando mucho en responder.",
            }
        except:
            rjson = {"codigoRetorno": 999, "mensajeRetorno": "\n\n" + response.text}