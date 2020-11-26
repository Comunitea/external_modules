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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models

class CarrierAccount(models.Model):
    _inherit = "carrier.account"

    is_mrw_account = fields.Boolean('MRW')
    mrw_account = fields.Char("MRW Client Code")
    mrw_franchise = fields.Char("MRW Franchise Code")
    mrw_saturday_delivery = fields.Selection([("S", "Yes"), ("N", "No")], default="N")
    mrw_frequency = fields.Selection([("1", "Frequency 1"), ("2", "Frequency 2")])
    mrw_830_delivery = fields.Selection([("S", "Yes"), ("N", "No")], default="N")
    mrw_delivery_hangle = fields.Selection(
        [("N", "No handle"), ("O", "Origin"), ("D", "Destination")], default="N"
    )
    mrw_delivery_pdo = fields.Selection(
        [
            ("N", "No Return"),
            ("O", "Payment on origin"),
            ("D", "Payment on destination"),
        ],
        default="N",
    )
    mrw_instant_notice = fields.Selection(
        [
            ("N", "No"),
            ("R", "Instant notice on picking"),
            ("E", "Instante notice on delivery"),
        ],
        default="N",
    )
    mrw_goods_type = fields.Selection(
        [
            ("DOC", "Documents"),
            ("MCV", "Samples with commercial value"),
            ("MSV", "Samples with no commercial value"),
            ("ATV", "High value"),
            ("BTV", "Low value"),
        ],
        string="Customs Duty",
    )
    mrw_mail_notification = fields.Boolean("Notify client by mail")
    mrw_phone_notification = fields.Boolean("Notify client by phone")
    mrw_notice_type = fields.Selection(
        [
            ("1", "Delivery"),
            ("2", "Tracking"),
            ("3", "Delivery on franchise"),
            ("4", "Alert before delivery"),
            ("5", "Alert after origin pick up"),
        ]
    )
    mrw_tracking_user = fields.Char("Tracking account")
    mrw_tracking_password = fields.Char("Tracking account password")
    mrw_tracking_service_url = fields.Char("Tracking service url")
    mrw_tracking_service_test_url = fields.Char("Tracking service test url")
