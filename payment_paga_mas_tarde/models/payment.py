# -*- coding: utf-8 -*-
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import urlparse

from odoo import api, fields, models
from odoo.addons.payment_paga_mas_tarde.controllers.main import PmtController


class AcquirerPagaMasTarde(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('pmt', 'Paga+Tarde')])
    pmt_public_key = fields.Char('Access Public Token', groups='base.group_user',
                                 help='Se encuentra en los datos de la tienda de su cuenta \
                                 de Paga+Tarde. Es imprescindible para autenticarse')
    pmt_private_key = fields.Char('Access Private Token', groups='base.group_user',
                                  help='Se encuentra en los datos de la tienda de su cuenta \
                                  de Paga+Tarde. Es imprescindible para autenticarse')

    @api.multi
    def pmt_get_form_action_url(self):
        """
        Devuelve la url del controller que se necesita para crear primero la orden en Paga+Tarde.
        No se puede acceder mediante el formulario directamente.
        :return:
        """
        return '/payment/pmt/order'

    @api.multi
    def pmt_form_generate_values(self, values):
        """
        Genera el diccionario con los datos que se necesitan para crear la orden en Paga+Tarde.
        :param values: los campos del formulario del boton de pago.
        :return: diccionario con los datos correctamente asociados.
        """
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        pmt_tx_values = dict(values)
        pmt_tx_values.update({
            "configuration": {
                "channel": {
                    "type": "ONLINE",
                    "assisted_sale": bool(0)
                },
                "urls": {
                    "ok": '%s' % urlparse.urljoin(base_url, PmtController._ok_url),
                    "ko": '%s' % urlparse.urljoin(base_url, PmtController._ko_url),
                    "cancel": '%s' % urlparse.urljoin(base_url, PmtController._cancel_url),
                    "authorized_notification_callback": '%s' % urlparse.urljoin(
                        base_url, PmtController._notification_url),
                    "rejected_notification_callback": '%s' % urlparse.urljoin(
                        base_url, PmtController._notification_url)
                }
            },
            "metadata": {
                "merchant_user_id": values.get('partner_id'),
                "merchant_shop_id": self.company_id.name,
                "additionalProp3": "",
            },
            "shopping_cart": {
                "order_reference": values.get('reference'),
                "promoted_amount": 0,
                "total_amount": values.get('amount'),
                "details": {
                    "shipping_cost": 0,
                    "products": [
                        {
                            "description": "N/D",
                            "quantity": 1,
                            "amount": values.get('amount'),
                        }
                    ]
                }
            },
            "user": {
                "full_name": values.get('partner_name'),
                "email": values.get('partner_email'),
                "fix_phone": values.get('partner_phone'),
                "mobile_phone": values.get('partner_phone'),
                "address": {
                    "full_name": values.get('partner_name'),
                    "address": values.get('partner_address'),
                    "city": values.get('partner_city'),
                    "zip_code": values.get('partner_zip'),
                    "country_code": values.get('partner_lang')[-2:],
                    "fix_phone": values.get('partner_phone'),
                    "mobile_phone": values.get('partner_phone'),
                },
                "billing_address": {
                    "full_name": values.get('billing_partner_name'),
                    "address": values.get('billing_partner_address'),
                    "city": values.get('billing_partner_city'),
                    "zip_code": values.get('billing_partner_zip'),
                    "country_code": values.get('partner_lang')[-2:],
                    "fix_phone": values.get('billing_partner_phone'),
                    "mobile_phone": values.get('billing_partner_phone'),
                },
                "shipping_address": {
                    "full_name": values.get('billing_partner_name'),
                    "address": values.get('billing_partner_address'),
                    "city": values.get('billing_partner_city'),
                    "zip_code": values.get('billing_partner_zip'),
                    "country_code": values.get('partner_lang')[-2:],
                    "fix_phone": values.get('billing_partner_phone'),
                    "mobile_phone": values.get('billing_partner_phone'),
                },
            }
        })

        return pmt_tx_values


class SaleOrder(models.Model):
    """
    Asocia el id de la orden de Paga+Tarde con el pedido de venta.
    """
    _inherit = 'sale.order'

    pmt_order_id = fields.Char(string='Paga+Tarde Order Id to confirm payment')


class TxPagaMasTarde(models.Model):
    """
    Asocia el id de la orden de Paga+Tarde con la transaccion generada.
    """
    _inherit = 'payment.transaction'

    pmt_tx_id = fields.Char('Transaction ID', help='ID operacion que permite identificar el pago en la cuenta \
                            de Paga+Tarde')
