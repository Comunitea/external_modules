# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    has_phantom_bom = fields.Boolean(compute='_compute_has_phantom_bom')

    def _compute_has_phantom_bom(self):
        for picking in self:
            has_phantom_bom = False
            if any([x.phantom_bom_component for x in picking.move_lines]):
                has_phantom_bom = True
            picking.has_phantom_bom = has_phantom_bom


class StockMove(models.Model):
    _inherit = 'stock.move'

    phantom_bom_component = fields.Boolean(
        compute='_compute_phantom_bom_component')

    def _compute_phantom_bom_component(self):
        for move in self:
            phantom_component = False
            if move.sale_line_id and move.sale_line_id.product_id != move.product_id:
                phantom_component = True
            move.phantom_bom_component = phantom_component
