# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    diff_level = fields.Integer('Picking diff level', compute ='get_diff_level',
                                          help="Picking diff level, sum of move diff level. If all done, all picks, if not remaining picks")

    @api.multi
    def get_diff_level(self):
        for order in self:
            pick = order.picking_ids.filtered(lambda x: x.state in ('done', 'confirmed', 'assigned') and x.picking_type_id.diff_level > 0)
            if all(p.state == 'done' for p in pick) or all(p.state != 'done' for p in pick):
                order.diff_level = sum(p.diff_level for p in pick)
            else:
                order.diff_level = sum(p.diff_level for p in pick.filtered(lambda x:x.state != 'done'))
