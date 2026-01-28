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
import logging

from requests import Session

from odoo import _
from odoo.exceptions import AccessError
from zeep import Client
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


class NcxRequest:
    """Interface between Nacex SOAP API and Odoo recordset
    Abstract Nacex API Operations to connect them with Odoo

    Not all the features are implemented, but could be easily extended with
    the provided API. We leave the operations empty for future.
    """
    def __init__(self, carrier):
        self.carrier = carrier
        self.client, self.history = self.create_client_ncx()

    def create_client_ncx(self):
        session = Session()
        session.verify = False

        try:
            transport = Transport(cache=SqliteCache(), session=session)
            history = HistoryPlugin()
            url = "http://pda.nacex.com/nacex_ws/soap?wsdl" # there is no test wsdl
            client = Client(url, transport=transport, plugins=[history])

            if client:
                return client, history
            else:
                raise AccessError(_("Not possible to establish a client."))
        except Exception as e:
            raise AccessError(_("Access error message: {}".format(e)))


    def putExpedicion(self, putExpedicion):
        _logger.info("putExpedicion: {}".format(putExpedicion))
        with self.client.settings(strict=False):

            service = self.client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                'http://pda.nacex.com/nacex_ws/soap')

            res = service.putExpedicion(
                **putExpedicion
            )

    def getEtiqueta(self, carrier_tracking_ref):

        getEtiqueta = {
            "String_1": self.ncx_account,
            "String_2": self.ncx_password,
            "String_3": carrier_tracking_ref,
            "String_4": self.ncx_printer_model
        }

        with self.client.settings(strict=False):

            service = self.client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                'http://pda.nacex.com/nacex_ws/soap')

            return service.getEtiqueta(**getEtiqueta)

    def cancelExpedicion(self, carrier_tracking_ref):
        arrayOfString_3 = [
            "expe_codigo={}".format(carrier_tracking_ref),
        ]

        cancelExpedicion = {
            "String_1": self.ncx_account,
            "String_2": self.ncx_password,
            "arrayOfString_3": arrayOfString_3
        }

        with self.client.settings(strict=False):

            service = self.client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                'http://pda.nacex.com/nacex_ws/soap')

            return service.cancelExpedicion(**cancelExpedicion)

    def getEstadoExpedicion(self, carrier_tracking_ref):
        getEstadoExpedicion = {
            "String_1": self.ncx_account,
            "String_2": self.ncx_password,
            "String_3": carrier_tracking_ref,
        }

        with self.client.settings(strict=False):

            service = self.client.create_service(
                '{urn:soap/types}nacexwsImplServiceSoapBinding',
                'http://pda.nacex.com/nacex_ws/soap')

            return service.getEstadoExpedicion(**getEstadoExpedicion)
