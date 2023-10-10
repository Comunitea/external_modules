# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

import logging
_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    _inherit = "stock.location"

    serial_location = fields.Many2one('stock.location', string='Ubicación de nº serie')

    def should_bypass_reservation(self):
        if self._context.get('bypass_reservation', False):
            return True
        return super().should_bypass_reservation()

    def write(self, vals):
        res = super().write(vals)
        if 'serial_location' in vals:
            for location in self:
                location.child_ids.write({'serial_location': location.serial_location})
        return res
