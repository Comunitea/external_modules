# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    need_packing_list = fields.Boolean('Packing list', default=False)
    packing_list_ids = fields.One2many('stock.packing.list', 'picking_id')

    @api.multi
    def open_stock_move_tree_for_packing(self):
        self.ensure_one()
        model_data = self.env['ir.model.data']
        tree_view = model_data.get_object_reference(
            'delivery_packing_list', 'stock_move_packing_list_tree')
        domain = [('picking_id', '=', self.id)]
        action = self.env.ref(
            'delivery_packing_list.stock_move_packing_list_tree_view_action').read()[0]
        action['views'] = {
            (tree_view and tree_view[1] or False, 'tree')}
        action['domain'] = domain
        action['context'] = {}
        return action




class StockMove(models.Model):
    _inherit = 'stock.move'

    def _default_uom(self):
        uom_categ_id = self.env.ref('product.product_uom_categ_kgm').id
        return self.env['product.uom'].search([('category_id', '=', uom_categ_id), ('factor', '=', 1)], limit=1)


    packing_list_id = fields.Many2one('stock.packing.list', 'Packing number', copy=False)
    weight = fields.Float(compute='_compute_weight')
    weight_uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly="1",
                                    help="Unit of measurement for Weight", default=_default_uom)

    @api.multi
    @api.depends('quantity_done')
    def _compute_weight(self):

        for ml in self:
            ml.product_uom._compute_quantity(ml.quantity_done, ml.product_id.uom_id) * ml.product_id.weight