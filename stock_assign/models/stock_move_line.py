# © 2025 Comunitea

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"


    def write(self, vals):

        moves = self.env['stock.move']
        if 'quantity' in vals:
            for move in self:
                if  vals["quantity"] < move.quantity_product_uom: 
                    moves |= move.move_id
            
        res = super().write(vals)
        if moves:
            moves._action_assign()
            
        return res

