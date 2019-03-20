# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError

class StockPackingList(models.Model):

    _name = 'stock.packing.list'
    _order = 'name'

    @api.multi
    @api.depends('stock_move_ids')
    def _compute_weight(self):

        for pack in self:
            weight = 0.00
            for ml in pack.stock_move_ids:
                weight += ml.product_uom._compute_quantity(ml.quantity_done, ml.product_id.uom_id) * ml.product_id.weight
            pack.weight = weight


    def _default_uom(self):
        uom_categ_id = self.env.ref('product.product_uom_categ_kgm').id
        return self.env['product.uom'].search([('category_id', '=', uom_categ_id), ('factor', '=', 1)], limit=1)

    weight = fields.Float(compute='_compute_weight')
    weight_uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly="1", help="Unit of measurement for Weight", default=_default_uom)
    name = fields.Char('Number', store=True, readonly=1)
    picking_id = fields.Many2one('stock.picking', 'Parent picking')
    stock_move_ids = fields.One2many('stock.move', 'packing_list_id', string='Contents')



    @api.model
    def default_get(self, fields):
        res = super(StockPackingList, self).default_get(fields)
        domain = [('picking_id', '=', res['picking_id'])]
        count = self.env['stock.packing.list'].search_count(domain)
        res['name'] = str(count+1).zfill(2)
        return res
