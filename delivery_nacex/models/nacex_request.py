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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See thefire
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import requests

from zeep import Client
from zeep import xsd
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport

NACEX_PRINTER_MODEL = [
    ("TECSV4_B", "TECSV4_B"),
    ("TECEV4_B", "TECEV4_B"),
    ("TECFV4_B", "TECFV4_B"),
    ("ZEBRA_B", "ZEBRA_B"),
    ("IMAGEN_B", "IMAGEN_B")
]
NACEX_PAYMENT_TYPE = [
    ("O", "Payment on origin"),
    ("D", "Payment on destination"),
    ("T", "Payment by a third party"),
]
NACEX_PACKAGE_TYPE = [
    ("0", "Documents"),
    ("1", "Nacex Bag"),
    ("2", "Nacex Cardboard Box"),
]
NACEX_POD_TYPE = [
    ("N", "No"),
    ("O", "Origin"),
    ("D", "Destination"),
    ("A", "Payment on pick up"),
]
NACEX_SERVICE_CODE = [
    ("01", "NACEX 10:00H"),
    ("02", "NACEX 12:00H"),
    ("03", "INTERDÍA"),
    ("04", "PLUS BAG 1"),
    ("05", "PLUS BAG 2"),
    ("06", "VALIJA"),
    ("07", "VALIJA IDA Y VUELTA"),
    ("08", "NACEX 19:00H"),
    ("09", "PUENTE URBANO"),
    ("10", "DEVOLUCIÓN ALBARÁN CLIENTE"),
    ("11", "NACEX 08:30H"),
    ("12", "DEVOLUCIÓN TALÓN"),
    ("14", "DEVOLUCIÓN PLUS BAG 1"),
    ("15", "DEVOLUCIÓN PLUS BAG 2"),
    ("17", "DEVOLUCIÓN E-NACEX"),
    ("21", "NACEX SÁBADO"),
    ("22", "CANARIAS MARÍTIMO"),
    ("24", "CANARIAS 24H"),
    ("25", "NACEX PROMO"),
    ("26", "PLUS PACK"),
    ("27", "E-NACEX"),
    ("28", "PREMIUM"),
    ("29", "NX-SHOP VERDE"),
    ("30", "NX-SHOP NARANJA"),
    ("31", "E-NACEX SHOP"),
    ("33", "C@MBIO"),
    ("48", "CANARIAS 48H"),
    ("88", "INMEDIATO"),
    ("90", "NACEX.SHOP"),
    ("91", "SWAP"),
    ("95", "RETORNO SWAP"),
]


class NacexRequest(object):
    def __init__(self, carrier):
        self.carrier_id = carrier
        self.path = "http://pda.nacex.com/nacex_ws/soap"
        self.client, self.history = self.create_client()
    
    def create_client(self):
        session = requests.Session()
        session.verify = False

        transport = Transport(cache=SqliteCache(), session=session)
        history = HistoryPlugin()
        url = self.path + "?wsdl"
        client = Client(url, transport=transport, plugins=[history])

        return client, history

    def create_shipment(self, vals):

        with self.client.settings(strict=False):

            service = self.client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                self.path)

            res = service.putExpedicion(
                **vals
            )
            return res

    def print_shipment(self, vals):
        with self.client.settings(strict=False):

            service = self.client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                self.path)

            label = service.getEtiqueta(**vals)
            return label

    def track_shipment(self, vals):
        with self.client.settings(strict=False):

            service = self.client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                self.path)

            res = service.getEstadoExpedicion(**vals)
            return res
    
    def cancel_shipment(self, vals):
        with self.client.settings(strict=False):

            service = self.client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                self.path)

            res = service.cancelExpedicion(**vals)
            return res
