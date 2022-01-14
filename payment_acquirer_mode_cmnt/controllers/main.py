# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import http
from odoo.http import request

from odoo.addons.sale.controllers.product_configurator import (
    ProductConfiguratorController,
)

_logger = logging.getLogger(__name__)


class WebsiteSale(ProductConfiguratorController):
    @http.route(
        [
            "/shop/payment/transaction/",
            "/shop/payment/transaction/<int:so_id>",
            "/shop/payment/transaction/<int:so_id>/<string:access_token>",
        ],
        type="json",
        auth="public",
        website=True,
    )
    def payment_transaction(
        self,
        acquirer_id,
        save_token=False,
        so_id=None,
        access_token=None,
        token=None,
        **kwargs
    ):
        # Ensure a payment acquirer is selected
        if not acquirer_id:
            return False

        try:
            acquirer_id = int(acquirer_id)
        except Exception:
            return False

        # Retrieve the sale order
        if so_id:
            env = request.env["sale.order"]
            domain = [("id", "=", so_id)]
            if access_token:
                env = env.sudo()
                domain.append(("access_token", "=", access_token))
            order = env.search(domain, limit=1)
        else:
            order = request.website.sale_get_order()

        # Ensure there is something to proceed
        if not order or (order and not order.order_line):
            return False

        assert order.partner_id.id != request.website.partner_id.id

        # Set order payment_method_id from the acquirer related payment method
        acquirer = request.env["payment.acquirer"].browse(acquirer_id)
        if acquirer and acquirer.payment_mode_id:
            order.payment_mode_id = acquirer.payment_mode_id.id
        else:
            order.payment_mode_id = order.partner_id.customer_payment_mode_id.id

        return super(WebsiteSale, self).payment_transaction(
            acquirer_id,
            save_token=False,
            so_id=None,
            access_token=None,
            token=None,
            **kwargs
        )
