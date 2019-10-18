# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class StockBatchPicking(models.Model):
    _inherit = 'stock.batch.picking'

    diff_level = fields.Integer('Picking diff level', compute ='get_diff_level',
                                          help="Batch picking diff level, sum of move diff level")

    @api.multi
    def get_diff_level(self):
        for batch in self:
            batch.diff_level = sum(pick.diff_level for pick in batch.picking_ids)


