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
import unidecode

from datetime import datetime

from requests import Session

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.addons import decimal_precision as dp
from zeep import Client
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport

import urllib.request

_logger = logging.getLogger(__name__)

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipment_reference = fields.Char("Shipment Reference")
    failed_shipping = fields.Boolean("Failed Shipping", default=False)
    carrier_type = fields.Selection(related="carrier_id.carrier_type")
    delivery_note = fields.Char(compute="_compute_delivery_note")

    def nacex_connect(self, method, data, etiqueta=False):
        ncx_url = "http://pda.nacex.com/nacex_ws/ws?method={}&data={}&user={}&pass={}".format(
            method,
            data,
            self.carrier_id.account_id.account,
            self.carrier_id.account_id.password
        )

        try:
            with urllib.request.urlopen(ncx_url) as response:
                html = response.read()
                if not etiqueta:
                    html = html.decode('UTF-8', 'ignore')
                    res = html.split('|')
                else:
                    res = html.decode('UTF-8', 'ignore').replace('\r\n', ' ')
                    if res.startswith("ERROR"):
                        return res.split('|')
                return res
        except Exception as e:
            _logger.error(_("Access error message: {}").format(e))
            return False

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
                nacex_data = "expe_codigo={}".format(
                    pick.carrier_tracking_ref,
                )

                res = self.nacex_connect("cancelExpedicion", nacex_data)

                if res:
                    _logger.info(
                        _("Canceled expedition: {}".format(res))
                    )

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

    def get_ncx_label(self, cod_exp):
        label = False

        nacex_data = "codExp={}|modelo={}".format(
            cod_exp,
            self.carrier_id.account_id.ncx_printer_model
        )

        res = self.nacex_connect("getEtiqueta", nacex_data, True)

        return res

    def _generate_ncx_label(self):

        def _unicode_url(chain):
            chain = unidecode.unidecode(chain.replace('|', ' '))
            return urllib.parse.quote_plus(chain)

        if self.carrier_tracking_ref:
            return self.print_ncx_label()
        self.check_delivery_address()

        if not self.carrier_service:
            raise UserError("Carrier service not selected.")
        if not self.carrier_id.account_id:
            raise UserError("Delivery carrier has no account.")

        data_0 = "del_cli={}|num_cli={}|tip_ser={}|tip_cob={}|ref_cli={}|tip_env={}|bul={}|kil={}|".format(
            self.carrier_id.account_id.ncx_delegation,
            self.carrier_id.account_id.ncx_client,
            self.carrier_service.carrier_code,
            self.carrier_id.account_id.ncx_payment_type,
            self.name,
            self.carrier_id.account_id.ncx_package_type,
            self.carrier_packages,
            round(self.carrier_weight),
        )

        if self.payment_on_delivery:
            pod_data = "ree={}|tip_ree={}|".format(
                self.pdo_quantity,
                self.carrier_id.account_id.ncx_pod_type
            )

            data_0 = "{}{}".format(data_0, pod_data)

        data_1 = "nom_ent={}|dir_ent={}{}|pais_ent={}|cp_ent={}|pob_ent={}|tel_ent={}|obs1={}|obs2={}|obs3={}|obs4={}".format(
            _unicode_url(self.partner_id.display_name),
            _unicode_url(self.partner_id.street) if self.partner_id.street else '',
            _unicode_url(self.partner_id.street2) if self.partner_id.street2 else '',
            urllib.parse.quote(self.partner_id.country_id.code),
            urllib.parse.quote(self.partner_id.zip),
            urllib.parse.quote(self.partner_id.city),
            _unicode_url(self.partner_id.phone) if self.partner_id.phone else _unicode_url(self.partner_id.mobile) if self.partner_id.mobile else '',
            _unicode_url(self.delivery_note[0:38]) if self.delivery_note else '',
            _unicode_url(self.delivery_note[38:75]) if self.delivery_note else '',
            _unicode_url(self.delivery_note[75:113]) if self.delivery_note else '',
            _unicode_url(self.delivery_note[113:151]) if self.delivery_note else '',
        )

        ncx_data = "{}{}".format(data_0, data_1)

        res = self.nacex_connect("putExpedicion", ncx_data)

        if res and res[0]=='ERROR':
            raise AccessError(_("Error message: {}").format(res[1]))
        elif res:

            self.write(
                {
                    "carrier_tracking_ref": res[0],
                    "shipment_reference": res[1],
                }
            )

            try:
                label = self.get_ncx_label(res[0])
            except Exception as e:
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
                        replaced_label = label.replace('} {', '}\n{')
                        file_b64 = base64.b64encode(str.encode(replaced_label))
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

            data = "expe_codigo={}".format(
                self.carrier_tracking_ref,
            )

            res = self.nacex_connect("getEstadoExpedicion", data)

            if res and res[0] != "ERROR":
                if res[4] and res[4] == 'OK':
                    self.delivered = True
                    return
            elif res and res[0] == "ERROR":
                _logger.error(_("Error: {}").format(res[1]))
                return
            else:
                _logger.error(_("Error: after requesting shipment status"))
                return

    def base64_url_decode(self, label):
        padding_factor = (4 - len(label) % 4) % 4
        label += "="*padding_factor
        return base64.b64decode(str(label).translate(dict(zip(map(ord, u'-_'), u'+/'))))
