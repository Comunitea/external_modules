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

    cex_result = fields.Text("CEX Result")

    @api.multi
    def number_of_packages_for_cex(self):
        self.ensure_one()
        # TODO check pack operation no disponible en v 12
        if self.has_packages:
            return len(self.move_line_ids.filtered(lambda ml: ml.result_package_id))

    def _prepare_cex_shipping(self):
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
        if self.carrier_id.file_format not in ("PDF", "ZPL"):
            raise UserError("Format file not supported by cex")
        if not self.carrier_service:
            raise UserError("Set service to the picking")
        if not self.carrier_weight or self.carrier_weight == 0.0:
            raise UserError("Set weight to the picking")
        data = {
            "solicitante": self.carrier_id.cex_solicitante,
            "canalEntrada": "",
            "numEnvio": "",
            "ref": self.origin[:20] if self.origin else self.name[:20],
            "refCliente": "",
            "fecha": date.today().strftime("%d%m%Y"),
            "codRte": self.carrier_id.cex_codRte,
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
            "reembolso": "{}".format(round(self.pdo_quantity,2)).replace(".", ",") if self.payment_on_delivery else "",
            "entrSabado": "",
            "seguro": "",
            "numEnvioVuelta": "",
            "listaBultos": listaBultos,
            "codDirecDestino": "",
            "password": "string",
            "listaInformacionAdicional": [
                {
                    "tipoEtiqueta": self.carrier_id.file_format == "PDF"
                    and "1"
                    or "2",
                    "etiquetaPDF": "",
                }
            ],
        }
        return data
