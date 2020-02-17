# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def force_set_qty_done(self):
        field = self._context.get('field', 'product_uom_qty')
        reset = self._context.get('reset', False)
        if reset:
            self.filtered(lambda x: x.quantity_done > 0 and x.state != 'done').write({field: 0})
        else:
            for move in self.filtered(lambda x: not x.quantity_done):
                move.quantity_done = move[field]

    @api.depends('state', 'picking_id')
    def _compute_is_initial_demand_editable(self):
        return super()._compute_is_initial_demand_editable()

    
    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super(StockMove, self)._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        vals.update(picking_type_id=self.picking_type_id.id)
        return vals
