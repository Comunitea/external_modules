# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from pprint import pprint


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    #_order = "removabarcode, barcode_dest, result_package_id desc, id"

    qty_available = fields.Float('Qty available', compute="get_qty_available")

    @api.depends('product_id', 'location_id')
    @api.multi
    def get_qty_available(self):
        code = self.mapped('picking_id').mapped('picking_type_code')
        if len(code)==1:
            code = code[0]
        else:
            code = 'internal'
        for line in self:
            if code == 'incoming':
                line.qty_available = line.ordered_qty
            else:
                line.qty_available = line.product_id.with_context(location=line.location_id.id).qty_available

    @api.multi
    def force_set_qty_done(self):
        field = self._context.get('field', 'product_uom_qty')
        reset = self._context.get('reset', False)
        if reset:
            self.filtered(lambda x: x.qty_done > 0 and x.state != 'done').write({'qty_done': 0})
        else:
            for move in self.filtered(lambda x: not x.qty_done):
                move.qty_done = move[field]
