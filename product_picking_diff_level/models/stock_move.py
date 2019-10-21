# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    diff_level = fields.Integer('Move diff level', compute ='get_diff_level', store=True,
                                          help="Move diff level, function diff level in product and location")

    @api.multi
    @api.depends('product_uom_qty')
    def get_diff_level(self):
        for move in self.filtered(lambda x: x.picking_id):
            #print ('{}: {}'.format(move.picking_id.name, move.diff_level))
            location_diff_level = move.location_id.diff_level if move.picking_type_id.code != 'incoming' else move.location_dest_id.diff_level
            move.diff_level = (min(1000, move.product_uom_qty) * move.product_id.diff_level + location_diff_level) * move.picking_type_id.diff_level



