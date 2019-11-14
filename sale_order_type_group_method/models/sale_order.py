# Copyright 2018 Omar Castiñeira Saavedra <omar@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    @api.onchange('type_id')
    def onchange_type_id(self):
        res = super(SaleOrder, self).onchange_type_id()
        for order in self:
            if order.type_id.invoice_group_method_id:
                order.invoice_group_method_id = (
                    order.type_id.invoice_group_method_id.id)
        return res

