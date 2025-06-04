##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2022 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
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
import json
import random
import string
import time
from datetime import datetime, timedelta

import requests
import urllib3

from odoo import api, fields, models, _
from odoo.exceptions import UserError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
_logger = logging.getLogger(__name__)


DHL_EXPRESS_API_URL = {
    "test": "https://wsbexpress.dhl.com/rest/sndpt/",
    "prod": "https://wsbexpress.dhl.com/rest/gbl/",
}


class DHLExpressRequest:

    def __init__(self, carrier):
        self.carrier = carrier
        api_env = "prod" if self.carrier.prod_environment else "test"
        self.url = DHL_EXPRESS_API_URL[api_env]
        self.username = self.carrier.dhl_express_login
        self.password = self.carrier.dhl_express_password
        self.dhl_express_account = self.carrier.dhl_express_account
    
    def setHeaders(self):

        auth_data = "{}:{}".format(
            self.username, self.password
        )
        auth_basic = "Basic " + str(base64.b64encode(auth_data.encode()).decode())

        headers = {
            "authorization": auth_basic,
            "content-type": "application/json",
            "cache-control": "no-cache",
        }

        return headers

    def _process_reply(self, url, payload):
        headers = self.setHeaders()
        try:
            response = requests.request(
                "POST", url, data=json.dumps(payload), headers=headers
            )
        except Exception as e:
            raise UserError(e)
        return response

    def _cancel_shipment(self, payload):
        url = "{}ShipmentDeleteRequest".format(
            self.url
        )
        response = self._process_reply(
            url,
            payload,
        )
        return response

    def _send_shipping(self, payload):
        url = "{}ShipmentRequest".format(
            self.url
        )
        response = self._process_reply(
            url,
            payload,
        )
        return response
    
    def _rate_shipping(self, payload):
        url = "{}RateRequest".format(
            self.url
        )
        response = self._process_reply(
            url,
            payload,
        )
        return response

    def _get_tracking_states(self, payload):
        url = "{}trackShipmentRequest".format(
            self.url
        )
        response = self._process_reply(
            url,
            payload,
        )
        return response
