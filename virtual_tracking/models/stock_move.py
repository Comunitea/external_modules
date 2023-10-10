# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
# from odoo.tools.float_utils import float_compare
from odoo.addons.alternative_tracking.models.product_product import TRACKING_VALUES

import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_available_serial_ids(self):
        self.ensure_one()
        self.available_serial_ids = self.move_line_ids.mapped("available_serial_ids")

    def _compute_serial_ids(self):
        for move in self:
            move.serial_name_ids = move.move_line_ids.mapped("serial_name_ids")
            move.serial_ids = move.move_line_ids.mapped("serial_ids")

    serial_ids = fields.One2many(comodel_name="stock.lot", compute="_compute_serial_ids")
    serial_name_ids = fields.One2many(comodel_name='virtual.serial', compute="_compute_serial_ids")

    available_serial_ids = fields.One2many(
        "stock.lot", compute=_get_available_serial_ids
    )
    lot_ids_string = fields.Text("Serial list to add")

    use_existing_lots = fields.Boolean(
        related="picking_id.picking_type_id.use_existing_lots", readonly=True
    )
    use_create_lots = fields.Boolean(
        related="picking_id.picking_type_id.use_create_lots", readonly=True
    )

    # virtual_tracking = fields.Boolean(related='product_id.virtual_tracking', store=True)
    template_tracking = fields.Selection(related='product_id.product_tmpl_id.template_tracking')#, store=True)
    # tracking = fields.Selection(selection=TRACKING_VALUES, default='none')


    def action_alternative_tracking_in_move_line(self):
        """Returns an action that will open a form view (in a popup) allowing to
        add lot for alternative tracking.
        """
        self.ensure_one()
        view = self.env.ref("alternative_tracking.view_stock_move_lot_names")
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

    def _action_done(self):
        return super()._action_done()
