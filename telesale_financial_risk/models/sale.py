# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.model
    # def ts_onchange_partner_id(self, partner_id):
    #     """
    #     Get warning messagges
    #     """
    #     res = super(SaleOrder, self).ts_onchange_partner_id(partner_id)
    #     order_t = self.env['sale.order']
    #     partner = self.env['res.partner'].browse(partner_id)

    #     order = order_t.new({'partner_id': partner_id,
    #                          'date_order': time.strftime("%Y-%m-%d"),
    #                          'pricelist_id':
    #                          partner.property_product_pricelist.id,
    #                          'early_payment_discount':
    #                              res['early_payment_discount']})
    #     res2 = order.onchange_partner_id_warning()
    #     warning = False

    #     if res2 and res2.get('warning', False):
    #         warning = res2['warning']['message']

    #     mode = 'warning'
    #     if partner.sale_warn == 'block':
    #         mode = 'block'
    #     res.update({
    #         'warning': warning,
    #         'mode': mode
    #     })
    #     return res

    @api.model
    def get_risk_msg(self, order_id):
        """
        Called before confirm_order_from_ui
        """
        exception_msg = ""
        if not self.env.context.get('bypass_risk', False):
            order = self.browse(order_id)
            partner = order.partner_id.commercial_partner_id
            if partner.risk_exception:
                exception_msg = _("Financial risk exceeded.\n")
            elif partner.risk_sale_order_limit and (
                    (partner.risk_sale_order + order.amount_total) >
                    partner.risk_sale_order_limit):
                exception_msg = _(
                    "This sale order exceeds the sales orders risk.\n")
            elif partner.risk_sale_order_include and (
                    (partner.risk_total + order.amount_total) >
                    partner.credit_limit):
                exception_msg = _(
                    "This sale order exceeds the financial risk.\n")
        return exception_msg
