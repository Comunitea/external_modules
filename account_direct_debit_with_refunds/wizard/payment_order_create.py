# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos S.L. (<http://comunitea.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class PaymentOrderCreate(models.TransientModel):
    _inherit = 'payment.order.create'

    @api.multi
    def extend_payment_order_domain(self, payment_order, domain):
        super(PaymentOrderCreate, self).extend_payment_order_domain(
            payment_order, domain)
        if payment_order.payment_order_type == 'debit':
            domain.remove(('debit', '>', 0))
        return True
