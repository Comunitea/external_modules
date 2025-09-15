# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
# from odoo.tools.float_utils import float_compare
from odoo.addons.virtual_tracking.models.product_product import TRACKING_VALUES

import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_available_serial_ids(self):
        # Devuelve los números de serie disponibles para este stock move
        self.ensure_one()
        spl = self.env["stock.lot"]
        if self.template_tracking != 'virtual':
            self.available_serial_ids = spl
        else:
            domain = [('product_id', '=', self.product_id.id), ('location_id', '=', self.location_id.serial_location_id.id)]
            # Si los movimientos previos tienen serial_ids solo pueden ser estos
            move_orig_ids = (self.origin_returned_move_id | self.move_orig_ids)
            serial_ids =  move_orig_ids.mapped("serial_ids")
            if serial_ids:
                domain += [("id", "in", serial_ids.ids)]
            self.available_serial_ids = spl.search(domain)

    def _compute_serial_ids(self):
        for move in self:
            move.serial_ids = move.move_line_ids.mapped("serial_ids")

    serial_ids = fields.One2many(comodel_name="stock.lot", compute="_compute_serial_ids")
    available_serial_ids = fields.One2many("stock.lot", compute=_get_available_serial_ids)
    template_tracking = fields.Selection(related='product_id.product_tmpl_id.template_tracking')#, store=True)


      

    def action_alternative_tracking_in_move_line(self):
        """Returns an action that will open a form view (in a popup) allowing to
        add lot for alternative tracking.
        """
        self.ensure_one()
        view = self.env.ref("virtual_tracking.view_stock_move_lot_names")
        return {
            "name": _("Detailed Lots"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "stock.move",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": self.id,
            "context": dict(
                self.env.context,
                default_product_id=self.product_id,
                default_usage=self.location_dest_id.usage,
            ),
        }
  
    def action_view_serials(self):
        action = self.env.ref("stock.action_production_lot_form").read()[0]
        action['context']= {'product_id': self.product_id.id,
                            'default_product_id': self.product_id.id,
                            'default_virtual_tracking': self.template_tracking == 'virtual'}
        action["domain"] = [("id", "in", self.serial_ids.ids)]
        return action

    def action_show_details(self):
        res = super().action_show_details()
        context = res['context']
        res['context'] = dict(context, recal_qty_done=True)
        return res
  
    @api.model
    def _run_fifo(self, move, quantity=None):
        # ???????????? Supongo para evitar errores # 
        move.ensure_one()
        if move.product_id.virtual_tracking and not quantity and not move.quantity_done:
            return 0
        return super()._run_fifo(move=move, quantity=quantity)

    def _run_valuation(self, quantity=None):
        # ???????????? Supongo para evitar errores # 
        self.ensure_one()
        if self.product_id.virtual_tracking and not quantity and not self.quantity_done:
            return 0
        return super()._run_valuation(quantity=quantity)
    
    """
    def write_new_serial_location_id(self):
        serial_ids = self.mapped("move_line_ids")
        for move_line in self.mapped('move_line_ids'):
            val = {'location_id': move_line.location_dest_id.serial_location_id.id}
            move_line.serial_ids.write(val)
        return True
    """
    def _action_done(self, cancel_backorder=False):
        return super()._action_done(cancel_backorder=cancel_backorder)

        # lo hago en el action done de stock move line
        """to_apply = self.filtered(lambda self: self.product_id.virtual_tracking and self.state == "done")
        if to_apply:
            to_apply.write_new_serial_location_id()
        """
        

    def should_bypass_tracking(self):
        sm = self.sudo()
        if sm.product_id.template_tracking != 'virtual':
            return True
        return sm.picking_type_id and sm.picking_type_id.bypass_tracking or False

        picking_type_id = sm.picking_type_id
        if not picking_type_id or picking_type_id.bypass_tracking: # No hay producciones or picking_type_id.code == 'production':
            return True

        #NO HAY PRODUCCIONES
        #if (sm.move_id.raw_material_production_id or sm.move_id.production_id):
        #    return True  # Los que vengan de producciones.                                          
        return False
    