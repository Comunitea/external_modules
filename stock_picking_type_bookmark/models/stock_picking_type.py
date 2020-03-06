# -*- coding: utf-8 -*-
# Copyright 2017 Comunitea - <comunitea@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

class StockPikcingTypeBookmark(models.Model):

    _name = 'stock.picking.type.bookmark'

    user_id = fields.Many2one('res.user', 'User', default=lambda self: self.env.user)
    picking_type_id = fields.Many2one('stock.picking.type', 'Picking type')

class StockPickingType(models.Model):

    _inherit = 'stock.picking.type'
    is_bookmarked = fields.Boolean(compute="compute_is_bookmark", string="Bookmarked")
    test = fields.Char(default="TEST")



    @api.model
    def search_read(self, domain, fields, offset=0, limit=None, order=None):
        if self._context.get('is_bookmark', False):
            domain1 = [('user_id', '=', self.env.user.id)]
            type_ids = self.env['stock.picking.type.bookmark'].search_read(domain1, ['picking_type_id'])
            if type_ids:
                ids = [x['picking_type_id'][0] for x in type_ids]
                domain += [('id', 'in', ids)]
        return super(StockPickingType, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    @api.multi
    def compute_is_bookmark(self):
        domain = [('user_id', '=', self.env.user.id), ('picking_type_id', 'in', self.ids)]
        type_ids = self.env['stock.picking.type.bookmark'].search(domain).mapped('picking_type_id')
        for type in type_ids:
            type.is_bookmarked = True

    @api.multi
    def compute_bookmark(self):
        to_unbookmark = self.filtered('is_bookmarked')
        to_bookmark = self - to_unbookmark
        to_unbookmark.delete_as_bookmark()
        to_bookmark.set_as_bookmark()

    @api.multi
    def set_as_bookmark(self):
        user = self.env.user.id
        for type in self:
            vals = {'user_id': user, 'picking_type_id': type.id}
            self.env['stock.picking.type.bookmark'].create(vals)

    @api.multi
    def delete_as_bookmark(self):
        user_id = self.env.user.id
        domain = [('user_id', '=', user_id), ('picking_type_id', 'in', self.ids)]
        self.env['stock.picking.type.bookmark'].search(domain).unlink()


