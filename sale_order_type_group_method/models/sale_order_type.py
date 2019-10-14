# Copyright 2018 Omar Castiñeira Saavedra <omar@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderType(models.Model):

    _inherit = "sale.order.type"

    invoice_group_method_id = fields.Many2one(
        string='Invoice Group Method',
        comodel_name='sale.invoice.group.method'
    )
