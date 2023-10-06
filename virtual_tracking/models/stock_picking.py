# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def apply_picking_serial_ids(self):
        self.ensure_one()
        for sml_id in self:
            sml_id.create_serial_ids_from_serial_names()

    @api.multi
    def get_sml_ids_serial_ids(self):
        return self.mapped('move_line_ids.serial_ids') # + self.mapped('move_line_ids.lot_id') 

    def show_tracking_serial_ids(self):
        action = self.env.ref(
            'stock.action_production_lot_form').read([])[0]
        action['domain'] = [('id', 'in', self.get_sml_ids_serial_ids().ids)]
        return action
