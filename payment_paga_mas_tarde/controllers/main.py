# -*- coding: utf-8 -*-
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import werkzeug
import json
import requests

from odoo import http
from odoo.http import request
from requests.auth import HTTPBasicAuth


class PmtController(http.Controller):
    """
    Controller del metodo de pago: Paga+Tarde
    """
    _ok_url = '/payment/pmt/result/order-approved'
    _ko_url = '/payment/pmt/result/order-rejected'
    _cancel_url = '/payment/pmt/result/order-cancelled'
    _notification_url = '/payment/pmt/result/notify'

    @http.route(['/payment/pmt/order'], type='http', auth="public", methods=['POST', 'GET', 'PUT'], csrf=False)
    def validate_order(self, **post):
        """
        Recoge los datos del formulario del boton de pago, crea un pedido de tipo paga+tarde con su formulario,
        guarda el id creado en nuestro pedido de venta y redirige al usuario a la web de de paga+tarde.
        :param post: los campos del formulario del boton de pago
        :return: redirige al usuario a la web de de paga+tarde
        """

        data = request.env.ref('payment_paga_mas_tarde.payment_acquirer_pmt').pmt_form_generate_values(post)
        pmt_private_key = data.get('pmt_private_key')
        pmt_public_key = data.get('pmt_public_key')
        request.session['pmt_tx_error'] = ''

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        #  Creamos la orden
        create_order = requests.post('https://api.pagamastarde.com/v2/orders', data=json.dumps(data),
                                     headers=headers, auth=HTTPBasicAuth(pmt_public_key, pmt_private_key))

        # Enviamos al usuario al formulario de paga+tarde y asociamos su order a sale_order
        if create_order.status_code == 201 and create_order.json().get('status', 'REJECTED') == 'CREATED':
            sale_order_id = request.session.get('sale_last_order_id')
            if sale_order_id:
                order_id = create_order.json().get('id', None)
                sale_order = request.env['sale.order'].sudo().browse(sale_order_id)
                sale_order.pmt_order_id = order_id

                action_url = create_order.json().get('action_urls')
                return werkzeug.utils.redirect(action_url['form'])

        # Algo ha salido mal por lo que volvemos a empezar
        request.session['pmt_tx_error'] = 'Vuelva a intentarlo'
        return werkzeug.utils.redirect('/shop/checkout')

    @http.route(['/payment/pmt/result/<page>'], type='http', auth="public", methods=['POST', 'GET', 'PUT'], csrf=False)
    def render(self, page):
        """
        Recoge las respuestas que envia el formulario de la web de de paga+tarde.
        En caso ok confirma el pedido de venta y la transaccion.
        :param page: nombre de la url que devuelve la web de de paga+tarde. Indica la accion a realizar
        :return: Si ok redirige a la confirmacion del pedido de venta en cualquier otro caso redirige al checkout
        """

        if 'approved' in str(page):
            # recopilamos datos necesarios
            sale_order_id = request.session.get('sale_last_order_id')
            if sale_order_id:
                sale_order = request.env['sale.order'].sudo().browse(sale_order_id)
                order_id = sale_order.pmt_order_id
                pmt_private_key = sale_order.payment_acquirer_id.pmt_private_key
                pmt_public_key = sale_order.payment_acquirer_id.pmt_public_key

                # confirmamos la orden
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }
                confirm_order = requests.put('https://api.pagamastarde.com/v2/orders/%s/confirm' % order_id,
                                             headers=headers, auth=HTTPBasicAuth(pmt_public_key, pmt_private_key))

                # Actulaizamos el pedido, la transaccion y los confirmamos
                if confirm_order.status_code == 200 and confirm_order.json().get('status', 'UNCONFIRMED') == 'CONFIRMED':
                    tx = sale_order.payment_tx_id
                    tx.write(
                        {'state': 'done', 'pmt_tx_id': order_id}
                    )
                    sale_order.with_context(send_email=True).action_confirm()
                    request.env['website'].sale_reset()
                    return werkzeug.utils.redirect('/shop/confirmation')
        elif 'cancelled' in str(page):
            request.session['pmt_tx_error'] = 'El pago ha sido cancelado'
        else:
            request.session['pmt_tx_error'] = 'El pago no se ha realizado'

        # Algo ha salido mal por lo que volvemos a empezar
        return werkzeug.utils.redirect('/shop/checkout')
