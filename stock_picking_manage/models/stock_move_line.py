# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from pprint import pprint


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    _order = "sequence, barcode, barcode_dest, result_package_id desc, id"



    @api.multi
    def _get_product_default_location_id(self):
        reserved_moves = self.filtered(lambda x: x.product_uom_qty != 0)
        for move in reserved_moves:
            move.default_product_dest_location_id = move.location_dest_id
            move.default_product_location_id = move.location_id
        for move in (self - reserved_moves):
            domain = [('putaway_id', '=', 1), ('product_product_id', '=', move.product_id.id)]
            spps = self.env['stock.product.putaway.strategy'].search(domain, limit=1)
            move.default_product_dest_location_id = spps.fixed_location_id or move.location_dest_id
            move.default_product_location_id = spps.fixed_location_id or move.location_id

    sequence = fields.Integer(string='Location order', default=0)
    barcode = fields.Char(related='location_id.barcode', store=True)
    barcode_dest = fields.Char(related='location_dest_id.barcode', store=True)
    default_product_location_id = fields.Many2one('stock.location', compute="_get_product_default_location_id", string="Default location")
    default_product_dest_location_id = fields.Many2one('stock.location', compute="_get_product_default_location_id", string="Default destination location")
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
                line.qty_available = line.product_id.with_context(location=line.location_id.id).qty_available_global

    @api.multi
    def force_set_qty_done(self):
        field = self._context.get('field', 'product_uom_qty')
        reset = self._context.get('reset', False)
        if reset:
            self.filtered(lambda x: x.qty_done > 0 and x.state != 'done').write({'qty_done': 0})
        else:
            for move in self.filtered(lambda x: not x.qty_done):
                move.qty_done = move[field]

    @api.multi
    def find_product_location(self):
        for move in self:
            put_ids = self.product_id.product_putaway_ids.filtered(lambda x:x.putaway_id.name == 'Put away')
            if put_ids:
                move.location_id = put_ids[0].fixed_location_id
            else:
                quants = self.env['stock.quant']._gather(move.product_id, move.move_id.location_id)
                if quants:
                    move.location_id = quants[0].location_id


    @api.model
    def create(self, vals):
        sequence = 0
        pt = self.env['stock.picking.type']
        if 'picking_type_id' in vals:
            pt = pt.browse(vals['picking_type_id'])
        order_vals = pt.get_move_order_field()
        if vals.get(order_vals['order_field'], False):
            obj = self.env[order_vals['model']].browse(vals[order_vals['order_field']])
            sequence = obj and obj[order_vals['field']] or 0
            vals.update(sequence=sequence)
        return super(StockMoveLine, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(StockMoveLine, self).write(vals)
        if 'location_id' in vals or 'location_dest_id' in vals:
            for ml in self:
                order_vals = ml.move_id.picking_type_id.get_move_order_field()
                if vals.get(order_vals['order_field'], False):
                    obj = self.env[order_vals['model']].browse(vals[order_vals['order_field']])
                    sequence = obj and obj[order_vals['field']] or 0
                    ml.sequence = sequence
        return res
