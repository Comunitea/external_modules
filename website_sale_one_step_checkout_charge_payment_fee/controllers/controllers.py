# -*- coding: utf-8 -*-
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.http import request
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleFee(WebsiteSale):

    @http.route()
    def payment(self, **post):
        """
        Replace default checkout payment to work with one step checkout payment.
        Only call super with context updated for no fee lines becouse do not works with payment fee.
        Context is necessary to do not delete payment fee lines in update_fee_line method.
        To work with payment_fee is necessary use payment_charge method.
        :param post: post values
        :return: call to super WebsiteSale payment
        """
        context = request.env.context.copy()
        context.update({'no_update_fee_line': True})
        request.env.context = context
        res = super(WebsiteSaleFee, self).payment(**post)
        return res

    @http.route(['/shop/checkout/charge_payment/'], type='json', auth='public', website=True, multilang=True)
    def payment_charge(self, **post):
        """
        Replace default checkout payment to work with one step checkout payment.
        Force to reload checkout page when choose a new acquirer for show it changed values
        :param post: payment_fee_id
        :return: True when reload page is necessary, False otherwise
        """
        order = request.website.sale_get_order()
        payment_fee_id = post.get('payment_fee_id')
        selected_acquirer = request.env['payment.acquirer'].browse(int(order.sudo().payment_acquirer_id.id))

        if not payment_fee_id:
            return

        if payment_fee_id:
            selected_acquirer = request.env['payment.acquirer'].browse(int(payment_fee_id))
            if selected_acquirer.id == order.sudo().payment_acquirer_id.id:
                return True

        order.sudo().update_fee_line(selected_acquirer.sudo())
        old_aqcuirer = order.sudo().payment_acquirer_id
        order.sudo().write({'payment_acquirer_id': payment_fee_id})

        values = {'reload_page': False}
        if selected_acquirer.charge_fee or not old_aqcuirer or old_aqcuirer.charge_fee:
            values['reload_page'] = True

        return values
