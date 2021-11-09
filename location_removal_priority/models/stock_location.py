# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    removal_priority = fields.Integer(
        string="Removal Priority", default=10,
        help="This priority applies when removing stock and incoming dates "
             "are equal.",
    )
