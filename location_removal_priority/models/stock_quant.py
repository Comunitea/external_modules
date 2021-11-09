# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    removal_priority = fields.Integer(
        related='location_id.removal_priority',
        readonly=True, store=True,
    )

    def _get_removal_strategy_order(self, removal_strategy=None):
        if removal_strategy == 'fifo':
            return 'in_date ASC NULLS FIRST, removal_priority ASC, id'
        elif removal_strategy == 'lifo':
            return 'in_date DESC NULLS LAST, removal_priority ASC, id desc'

        else:
            return super()._get_removal_strategy_order(
                removal_strategy=removal_strategy)
