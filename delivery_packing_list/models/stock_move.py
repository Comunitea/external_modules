# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _default_uom(self):
        uom_categ_id = self.env.ref('product.product_uom_categ_kgm').id
        return self.env['product.uom'].search(
            [('category_id', '=', uom_categ_id), ('factor', '=', 1)], limit=1)

    sscc_ids = fields.Many2many(
        'stock.move.line.sscc', 'operation_sscc_rel', 'move_line_id',
        'sscc_id')

    packing_list_id = fields.Many2one('stock.packing.list', 'Packing number',
                                      copy=False)
    weight = fields.Float(compute='_compute_weight')
    volume = fields.Float(compute='_compute_weight')
    weight_uom_id = fields.Many2one(
        'product.uom', string='Unit of Measure', required=True, readonly="1",
        help="Unit of measurement for Weight", default=_default_uom)

    @api.multi
    def _compute_weight(self):
        for ml in self:
            qty = ml.product_uom._compute_quantity(
                ml.quantity_done, ml.product_id.uom_id)
            ml.weight = ml.product_id.weight * qty
            ml.volume = ml.product_id.volume * qty


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _default_uom(self):
        uom_categ_id = self.env.ref('product.product_uom_categ_kgm').id
        return self.env['product.uom'].search(
            [('category_id', '=', uom_categ_id), ('factor', '=', 1)], limit=1)

    packing_list_id = fields.Many2one(
        'stock.packing.list', 'Packing number', copy=False)
    weight = fields.Float(compute='_compute_weight')
    volume = fields.Float(compute='_compute_weight')
    weight_uom_id = fields.Many2one(
        'product.uom', string='Unit of Measure', required=True, readonly="1",
        help="Unit of measurement for Weight", default=_default_uom)

    @api.multi
    def _compute_weight(self):
        for ml in self:
            qty = ml.product_uom._compute_quantity(
                ml.quantity_done, ml.product_id.uom_id)
            ml.weight = ml.product_id.weight * qty
            ml.volume = ml.product_id.volume * qty

    @api.multi
    @api.onchange('packing_list_id')
    def onchange_packing_list_id(self):
        for move in self:
            move.move_line_ids.write({
                'packing_list_id': move.packing_list_id and
                move.packing_list_id.id or False})
