# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

class StockBatchPickingCreator(models.TransientModel):
    """Create a stock.picking.batch from stock.picking
    """

    _inherit = 'stock.picking.batch.creator'

    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', required=True)



    def get_picking_type_id(self):
        domain = [('id', 'in', self._context.get('active_ids', []))]
        picking_type_id = self.env['stock.picking'].search_read(domain, ['picking_type_id'], limit=1)

        if not picking_type_id:
            return False
        return picking_type_id[0]['picking_type_id'] and picking_type_id[0]['picking_type_id'][0] or False

    def _prepare_stock_batch_picking(self):
        res = super()._prepare_stock_batch_picking()
        if self.picking_type_id:
            res['picking_type_id'] = self.picking_type_id.id
        return res

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res['picking_type_id'] = self.get_picking_type_id()
        return res

    @api.multi
    def action_create_batch(self):
        """ Create a batch picking  with selected pickings after having checked
        that they are not already in another batch or done/cancel.
        """

        domain = [
            ('id', 'in', self.env.context['active_ids']),
            ('batch_id', '=', False),
            ('state', 'not in', ('cancel', 'done')),
        ]
        if not self.batch_by_group:
            type_ids = self.env['stock.picking'].search(domain).mapped('picking_type_id')
            if len(type_ids) > 1:
                raise ValidationError (_('Only one picking type if not grouped'))

        return super().action_create_batch()