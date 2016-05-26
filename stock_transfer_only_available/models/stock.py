# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, api


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    @api.model
    def _search(self, args, offset=0, limit=0, order=None, count=False,
                access_rights_uid=None):
        if self._context.get('product_id', False) and \
                self._context.get('location_id', False):
            location = self._context.get('location_id', False)
            stock_ids = [x.lot_stock_id.id
                         for x in self.env['stock.warehouse'].search([])]
            is_stock = self.env['stock.location'].search(
                [('id', 'child_of', stock_ids), ('id', '=', location)])
            if is_stock:
                quants = self.env['stock.quant'].search(
                    [('location_id', '=', self._context.get('location_id')),
                     ('product_id', '=', self._context.get('product_id')),
                     ('lot_id', '!=', False)])
                lot_ids = [x.lot_id.id for x in quants]
                args = [('id', 'in', lot_ids)] + args
        return super(StockProductionLot, self)._search(
            args, offset, limit, order, count=count,
            access_rights_uid=access_rights_uid)
