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
import re
import time
import base64
import json
import string
import random
from datetime import datetime, timedelta

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .dhl_express_request import DHLExpressRequest
_logger = logging.getLogger(__name__)

class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(
        selection_add=[("dhl_express", "DHL Express")], ondelete={"dhl_express": "set default"}
    )
    dhl_express_account = fields.Char("DHL Account")
    dhl_express_login = fields.Char("DHL Login")
    dhl_express_password = fields.Char("DHL Password")
    dhl_express_label_template = fields.Selection(
        [
            ("ECOM26_84_A4_001", "ECOM26_84_A4_001"),
            ("ECOM26_84_001", "ECOM26_84_001"),
            ("ECOM_TC_A4", "ECOM_TC_A4"),
            ("ECOM26_A6_002", "ECOM26_A6_002"),
            ("ECOM26_84CI_001", "ECOM26_84CI_001"),
            ("ECOM_A4_RU_002", "ECOM_A4_RU_002"),
            ("ECOM26_A6_002", "ECOM26_A6_002"),
            ("ECOM26_84CI_002", "ECOM26_84CI_002"),
            ("ECOM26_84CI_003", "ECOM26_84CI_003"),
            ("ECOM26_64_001", "ECOM26_64_001"),
        ],
        default="ECOM26_64_001",
    )
    dhl_express_service = fields.Selection(
        [
            ("Y", "DHL EXPRESS 12:00 (NO DOCUMENT)"),
            ("T", "DHL EXPRESS 12:00"),
            ("M", "DHL EXPRESS 10:30 (USA) (NO DOCUMENT)"),
            ("L", "DHL EXPRESS 10:30 (USA)"),
            ("E", "DHL EXPRESS 9:00 (NO DOCUMENT)"),
            ("K", "DHL EXPRESS 9:00"),
            ("X", "EXPRESS DOCUMENT"),
            ("P", "DHL EXPRESS WORLDWIDE (NO DOCUMENT)"),
            ("D", "DHL EXPRESS WORLDWIDE (DOCUMENTO)"),
            ("W", "ECONOMY SELECT -DOC-"),
            ("H", "ECONOMY SELECT -NON DOC-"),
            ("U", "DHL EXPRESS WORLDWIDE (UE) (DOCUMENTS)"),
            ("N", "DHL EXPRESS SPAIN (DOCUMENTS)"),
        ],
        default="Y",
    )
    dhl_express_documents = fields.Selection(
        [
            ("DOCUMENTS", "DOCUMENTS"),
            ("NON_DOCUMENTS", "NON_DOCUMENTS"),
        ],
        default="NON_DOCUMENTS",
    )
    dhl_express_daily_picking = fields.Boolean(string="Daily Picking", default=True)
    dhl_express_plt_service = fields.Boolean(string="PLT Service", default=False)
    dhl_express_customs_duty = fields.Boolean(string="Customs Duty", default=False)
    dhl_express_file_format = fields.Selection([("pdf", "PDF"), ("zpl", "zpl")], default="pdf", required=True)
    allowed_pricelist_ids = fields.Many2many(comodel_name="product.pricelist", string="Allowed pricelist")
    dhl_uk_importer = fields.Selection([
        ('us', 'US'),
        ('client', 'CLIENT')
    ], string='Add UK importer')
    debug_in_chatter = fields.Boolean('Debug in chatter', default=False)

    def dhl_express_reset_pickup_request(self):
        pickup_requested = self.env["ir.config_parameter"].sudo().get_param("delivery_dhl_express.pickup_requested", False)
        if pickup_requested and pickup_requested == "True":
            self.env["ir.config_parameter"].sudo().set_param("delivery_dhl_express.pickup_requested", "False")

    def dhl_express_get_tracking_link(self, picking):
        return "https://mydhl.express.dhl/es/es/tracking.html#/results?id={}".format(
            picking.carrier_tracking_ref
        )

    def get_message_reference(self, stringLength=8):
        lettersAndDigits = string.ascii_letters + string.digits
        return "".join((random.choice(lettersAndDigits) for i in range(stringLength)))

    def dhl_express_send_shipping(self, pickings):
        return [self.dhl_express_create_shipping(p) for p in pickings]

    def dhl_express_create_shipping(self, picking):
        dhl_express_request = DHLExpressRequest(self)
        vals = self._prepare_dhl_express_shipping(picking)
        response = dhl_express_request._send_shipping(vals)
        vals.update({"tracking_number": False, "exact_price": 0})

        if "ShipmentResponse" in response.json():
            response = response.json()["ShipmentResponse"]
            if "ShipmentIdentificationNumber" not in response:
                raise UserError(
                    "Error: {}".format(response["Notification"][0]["Message"])
                )
            picking.carrier_tracking_ref = "{}".format(response["ShipmentIdentificationNumber"])
            vals["tracking_number"] = "{}".format(response["ShipmentIdentificationNumber"])

            if response["LabelImage"]:
                if picking.carrier_id.dhl_express_file_format == "pdf":
                    attachment_id = self.env["ir.attachment"].create(
                        {
                            "name": "dhl_label: {}".format(picking.name),
                            "type": "binary",
                            "datas": response["LabelImage"][0]["GraphicImage"],
                            "res_model": picking._name,
                            "res_id": picking.id,
                            "mimetype": "application/pdf",
                        }
                    )
                else:
                    attachment_id = self.env["ir.attachment"].create(
                        {
                            "name": "dhl_label: {}.{}".format(picking.name, response["LabelImage"][0]["LabelImageFormat"]),
                            "type": "binary",
                            "datas": response["LabelImage"][0]["GraphicImage"],
                            "res_model": picking._name,
                            "res_id": picking.id,
                            "mimetype": "text/plain",
                        }
                    )

                if attachment_id:
                    msg = _("Label(s) retrieved from DHL EXpress.")
                    picking.message_post(body=msg, attachment_ids=[attachment_id.id])

            if response["PackagesResult"]:
                shipment_reference = ""
                for package in response["PackagesResult"]["PackageResult"]:
                    shipment_reference += "{} ".format(
                        package["TrackingNumber"]
                    )
                picking.write({"dhl_express_shipment_reference": shipment_reference})

            pickup_requested = self.env["ir.config_parameter"].sudo().get_param("delivery_dhl_express.pickup_requested", False)

            if not pickup_requested or pickup_requested == "False":
                self.env["ir.config_parameter"].sudo().set_param("delivery_dhl_express.pickup_requested", "True")
            return vals
        else:
            raise UserError("Error processing the response: {}".format(response))

    def _prepare_dhl_express_shipping(self, picking):
        self.ensure_one()
        receiving_partner = picking.partner_id
        picking.compute_request_date()

        # If there are invoices we get the report for them
        # otherwise we send the sale.order pdf
        pdf_invoices = []
        inv_report = self.env["ir.actions.report"]._get_report_from_name(
            "account.report_invoice_with_payments"
        )
        inv_number = picking.name
        non_canceled_invoices = picking.sale_id.invoice_ids.filtered(lambda x: x.state not in ['cancel'])
        if non_canceled_invoices:
            inv_number = picking.sale_id.invoice_ids[0].name
            for invoice in non_canceled_invoices:
                pdf_invoices.append(
                    inv_report.sudo()._render_qweb_pdf([invoice.id])[0] or False
                )
        else:
            pdf_invoices.append(
                self.env['ir.actions.report'].sudo()
                ._render_qweb_pdf('sale.action_report_saleorder', res_ids=picking.sale_id.id)[0]
                or False
            )
            inv_number = picking.sale_id.name

        RequestedPackages = []
        # Picking field: notas.
        picking_packages = 1
        for package in picking.package_ids:
            package_info = {
                "@number": picking_packages,
                "Weight": package.shipping_weight,
                "Dimensions": {
                    "Length": package.package_type_id.packaging_length if package.package_type_id else package.pack_length,
                    "Width": package.package_type_id.width if package.package_type_id else package.width,
                    "Height": package.package_type_id.height if package.package_type_id else package.height,
                },
                "CustomerReferences": "{}".format(package.name),
            }
            RequestedPackages.append(package_info)
            picking_packages += 1

        DocumentImage = []
        for pdf_invoice in pdf_invoices:
            DocumentImage.append({
                    "DocumentImageType": "CIN",
                    "DocumentImage": "%s" % base64.b64encode(pdf_invoice).decode("utf8") if pdf_invoice else False,
                    "DocumentImageFormat": "PDF",
            })

        attachment_ids = self.env['ir.attachment'].search([
            ("res_model", "=", picking._name),
            ("res_id", "=", picking.id),
            ("type", "=", "binary"),
        ])

        for attachment_id in attachment_ids.filtered(lambda x: "Label: " not in x.name):
            DocumentImage.append({
                "DocumentImageType": "NAF",
                "DocumentImage": "%s" % base64.b64encode(attachment_id.datas).decode("utf8") if attachment_id.datas else False,
                "DocumentImageFormat": "PDF",
            })

        DocumentImages = {
            "DocumentImage": DocumentImage
        }

        ExportLineItem = []
        item_number = 1
        for move in picking.move_ids:
            move_info = {
                "ItemNumber": item_number,
                "CommodityCode": move.product_id.dhl_express_code,
                "Quantity": int(move.product_uom_qty),
                "QuantityUnitOfMeasurement": move.product_id.dhl_express_measurement,
                "ItemDescription": move.product_id.dhl_express_description,
                "UnitPrice": round(move.sale_line_id.price_total/move.product_uom_qty, 3),
                "NetWeight": move.product_id.weight,
                "GrossWeight": move.product_id.weight, # TODO review the net and gross weight fields.
                "ManufacturingCountryCode": move.product_id.origin_country_id.code,
            }
            ExportLineItem.append(move_info)
            item_number += 1

        ExportLineItems = {
            'ExportLineItem': ExportLineItem
        }

        Service = []

        if self.dhl_express_plt_service:
            Service.append({
                "ServiceType": "WY",
            })

        if self.dhl_express_customs_duty or (picking.sale_id.pricelist_id.dhl_express_ddp and receiving_partner.country_id.code == 'US'):
            Service.append({
                "ServiceType": "DD",
            })

        SpecialServices = []

        if len(Service):
            SpecialServices = {
                "Service": Service
            }

        pickup_requested = self.env["ir.config_parameter"].sudo().get_param("delivery_dhl_express.pickup_requested", False)
        dhl_service = self.dhl_express_service

        CompanyRegistrationNumber = [{
            "Number" : "{}".format(self.env.user.company_id.vat),
            "NumberTypeCode": "VAT",
            "NumberIssuerCountryCode": self.env.user.company_id.country_id.code or "ES"
        }]

        if receiving_partner.country_id.code == 'GB' and self.env.user.company_id.eori_number:
            CompanyRegistrationNumber.append(
                {
                    "Number" : "{}".format(self.env.user.company_id.eori_number),
                    "NumberTypeCode": "EOR",
                    "NumberIssuerCountryCode": self.env.user.company_id.country_id.code or "ES"
                }
            )

        payload = {
            "ShipmentRequest": {
                "RequestedShipment": {
                    "ShipmentInfo": {
                        "DropOffType": "REGULAR_PICKUP"
                        if self.dhl_express_daily_picking or pickup_requested == "True"
                        else "REQUEST_COURIER",
                        "ServiceType": dhl_service,
                        "Account": "{}".format(
                            self.dhl_express_account
                        ),
                        "Currency": "EUR",
                        "UnitOfMeasurement": "SI",
                        "LabelType": self.dhl_express_file_format.upper(),
                        "PackagesCount": picking_packages,
                        "LabelTemplate": self.dhl_express_label_template,
                        "PaperlessTradeEnabled": 1 if dhl_service not in ['U', 'N'] else False, #DOM (N) and ECX (U) goes False
                        "DocumentImages": DocumentImages,
                        "SpecialServices": SpecialServices,
                    },
                    "ShipTimestamp": picking.request_date,
                    "PaymentInfo": "DDP" if self.dhl_express_customs_duty or (picking.sale_id.pricelist_id.dhl_express_ddp and receiving_partner.country_id.code == 'US') else "DAP",
                    "InternationalDetail": {
                        "Commodities": {
                            "Description": "{}".format(picking.name.upper())
                        },
                        "Content": self.dhl_express_documents if dhl_service not in ["Y", "M", "E", "P", "H"] else "NON_DOCUMENTS",
                        "ExportDeclaration": {
                            "ExportReason": "Commercial Sold",
                            "InvoiceNumber": inv_number,
                            "ExportReasonType": "PERMANENT",
                            "ShipmentPurpose": "COMMERCIAL",
                            "ExportLineItems": ExportLineItems,
                            "InvoiceDate": picking.sale_id.date_order.strftime("%Y-%m-%d"),
                        },
                    },
                    "Ship": {
                        "Shipper": {
                            "Contact": {
                                "PersonName": "{}".format(
                                    self.env.user.company_id.name.upper()
                                ),
                                "CompanyName": "{}".format(
                                    self.env.user.company_id.name.upper()
                                ),
                                "PhoneNumber": "{}".format(
                                    self.env.user.company_id.phone or ""
                                ),
                                "EmailAddress": self.env.user.company_id.email,
                            },
                            "Address": {
                                "StreetLines": "{}".format(
                                    self.env.user.company_id.street
                                ),
                                "StreetLines2": "{}".format(
                                    self.env.user.company_id.street2 or "N/A"
                                ),
                                "City": "{}".format(
                                    self.env.user.company_id.city.upper()
                                ),
                                "PostalCode": self.env.user.company_id.zip,
                                "CountryCode": "{}".format(
                                    self.env.user.company_id.country_id.code or "ES"
                                ),
                            },
                            "RegistrationNumbers": {
                                "RegistrationNumber": CompanyRegistrationNumber
                            }
                        },
                        "Recipient": {
                            "Contact": {
                                "PersonName": "{}".format(
                                    receiving_partner.name.upper()
                                ),
                                "CompanyName": "{}".format(
                                    receiving_partner.parent_id.name.upper()
                                    if receiving_partner.parent_id
                                    else receiving_partner.name.upper()
                                ),
                                "PhoneNumber": "{}".format(
                                    receiving_partner.phone
                                    or receiving_partner.mobile
                                    or receiving_partner.commercial_partner_id.phone
                                    or receiving_partner.commercial_partner_id.mobile
                                ),
                                "EmailAddress": "{}".format(
                                    receiving_partner.email
                                    or receiving_partner.commercial_partner_id.email
                                ),
                            },
                            "Address": {
                                "StreetLines": "{}".format(receiving_partner.street),
                                "StreetLines2": "{}".format(
                                    receiving_partner.street2 or "N/A"
                                ),
                                "StreetLines3": "{}".format(
                                    "N/A"
                                ),
                                "City": "{}".format(receiving_partner.city.upper()),
                                "PostalCode": receiving_partner.zip,
                                "CountryCode": "{}".format(
                                    receiving_partner.country_id.code
                                ),
                            },
                        },
                    },
                    "Packages": {"RequestedPackages": RequestedPackages},
                }
            }
        }

        if receiving_partner.country_id.code != "ES":
            payload["ShipmentRequest"]["RequestedShipment"]["InternationalDetail"]["Commodities"]["CustomsValue"] = round(picking.sale_id.amount_total, 3)

        services = picking.sale_id.order_line.filtered(lambda x: x.product_id.type == 'service')
        if services:
            OtherCharge = []
            discount_total = sum(service.price_total for service in services.filtered(lambda x: x.product_id.dhl_service_type == 'discount'))
            if discount_total and discount_total != 0:
                OtherCharge.append({
                    "Caption": "Discount",
                    "ChargeValue": "{}".format(round(discount_total, 3)),
                    "ChargeType": "SOTHR"
                })
            freight_total = sum(service.price_total for service in services.filtered(lambda x: x.product_id.dhl_service_type == 'delivery'))
            if freight_total and freight_total != 0:
                OtherCharge.append({
                    "Caption": "Freight",
                    "ChargeValue": "{}".format(round(freight_total, 3)),
                    "ChargeType": "FRCST"
                })
            other_total = sum(service.price_total for service in services.filtered(lambda x: x.product_id.dhl_service_type == 'other'))
            if other_total and other_total != 0:
                OtherCharge.append({
                    "Caption": "Logistics/Other charges",
                    "ChargeValue": "{}".format(round(other_total, 3)),
                    "ChargeType": "LOGST"
                })
            if len(OtherCharge) > 0:
                payload["ShipmentRequest"]["RequestedShipment"]["InternationalDetail"]["ExportDeclaration"]["OtherCharges"] = {
                    'OtherCharge': OtherCharge
                }

        return payload

    # This method only cancels pickups not ShipmentRequests, so it's useless at the moment.
    def dhl_express_cancel_shipment(self, pickings):
        for picking in pickings.filtered("dhl_express_shipment_reference"):
            picking.dhl_express_shipment_reference = None
            """ if not picking.dhl_express_confirmation_number:
                msg = _("There is no DispatchConfirmationNumber associated with this picking.")
                picking.message_post(body=msg)
                continue
            dhl_express_request = DHLExpressRequest(self)
            payload = self._prepare_dhl_express_cancel(picking)
            response = dhl_express_request._cancel_shipment(payload)

            if "DeleteResponse" in response.json():
                response = response.json()["DeleteResponse"]
                notifications = response.get("Notification", False)
                for notification in notifications:
                    if notification.get("@code", False) == "0":
                        picking.write(
                            {"dhl_express_shipment_reference": None}
                        )
                    msg = _("DHL Express Response: {} - {}".format(notification.get("@code", False), notification.get("Message", False)))
                    picking.message_post(body=msg)
            elif "reasons" in response.json():
                msg = _("DHL Express Response: {}".format(response.json()["reasons"][0].get("msg", False)))
                picking.message_post(body=msg)
                continue """


    def _prepare_dhl_express_cancel(self, picking):
        self.ensure_one()
        payload = {
            "ShipmentDeleteRequest": {
                "DeleteRequest": {
                    "PickupDate": picking.request_date,
                    "PickupCountry": "{}".format(
                        self.env.user.company_id.country_id.code or "ES"
                    ),
                    "DispatchConfirmationNumber": picking.dhl_express_confirmation_number,
                    "RequestorName": "{}".format(
                        self.env.user.company_id.name.upper()
                    ),
                }
            }
        }

        return payload

    def dhl_express_tracking_state_update(self, picking):
        """Tracking state update"""
        self.ensure_one()
        if not picking.carrier_tracking_ref:
            return

        dhl_express_request = DHLExpressRequest(self)
        payload = self._prepare_dhl_express_tracking(picking)
        response = dhl_express_request._get_tracking_states(payload)

        if response.json() and "trackShipmentRequestResponse" in response.json():
            response = response.json()["trackShipmentRequestResponse"]
            awbinfoitem = response["trackingResponse"]["TrackingResponse"]["AWBInfo"][
                "ArrayOfAWBInfoItem"
            ]
            if "ShipmentInfo" in awbinfoitem:
                if "ShipmentEvent" in awbinfoitem["ShipmentInfo"]:
                    delivery_status = awbinfoitem["ShipmentInfo"]["ShipmentEvent"][
                        "ArrayOfShipmentEventItem"
                    ]["ServiceEvent"]["EventCode"]
                    if delivery_status == "OK":
                        picking.write({
                            'delivery_state': 'customer_delivered'
                        })
            else:
                _logger.error(
                    _("Access error message: {}").format(
                        awbinfoitem["Status"]["ActionStatus"]
                    )
                )
                return

    def _prepare_dhl_express_tracking(self, picking):
        self.ensure_one()
        payload = {
            "trackShipmentRequest": {
                "trackingRequest": {
                    "TrackingRequest": {
                        "Request": {
                            "ServiceHeader": {
                                "MessageTime": "{}".format(
                                    picking.request_date.replace("GMT", "")
                                ),
                                "MessageReference": "{}".format(
                                    self.get_message_reference(32)
                                ),
                            }
                        },
                        "AWBNumber": {
                            "ArrayOfAWBNumberItem": picking.carrier_tracking_ref
                        },
                        "LevelOfDetails": "LAST_CHECKPOINT_ONLY",
                    }
                }
            }
        }

        return payload
