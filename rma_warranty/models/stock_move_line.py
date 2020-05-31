# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models
from dateutil.relativedelta import relativedelta


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    def _action_done(self):
        res = super()._action_done()
        ## El action done de odoo tiene un bug y devuelve un self con un elemento borrado 
        # si se procesa mas cantidad que la que se reserva por lo que falla aquí
        for move_line in self.filtered(lambda r: r.exists()
                        and r.picking_id.picking_type_id.code == "outgoing"):
            if move_line.lot_id and move_line.product_id.warranty_duration:
                warranty_termination = move_line.date + relativedelta(
                    days=move_line.product_id.warranty_duration
                )
                move_line.lot_id.warranty_termination = (
                    warranty_termination.date()
                )
        return res
