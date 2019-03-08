# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'


    @api.multi
    def action_confirm_for_pda(self):
        for move in self:
            move._action_confirm()

    @api.multi
    def action_assign_for_pda(self):
        for move in self:
            move._action_assign()

    @api.multi
    def force_assign_for_pda(self):
        for move in self:
            move._force_assign()

    @api.multi
    def action_done_for_pda(self):
        for move in self:
            if not move.product_uom_qty:
                move.product_uom_qty = move.quantity_done
            move._action_done()

    @api.multi
    def action_cancel_for_pda(self):
        for move in self:
            move._action_cancel()

    @api.multi
    def do_unreserve_for_pda(self):
        for move in self:
            move._do_unreserve()

    @api.multi
    def force_set_qty_done_all(self):
        for move in self:
            move.quantity_done = move.product_uom_qty



    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        #if not self.picking_id:
        #    vals.update(location_dest_id=self.location_dest_id.id, location_id=self.location_id.id)
        return vals