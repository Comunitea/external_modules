# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

from .stock_move import DOMAIN_NOT_STATE

class ProcurementGroup(models.Model):

    _inherit = 'procurement.group'


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super()._prepare_stock_moves(picking)
        for val in res:
            val['purchase_id'] = self.order_id.id
            val['shipping_id'] = self.order_id.partner_id.id
        return res


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def _get_move_line_ids(self):

        for order in self:
            domain = self.get_moves_domain()
            order.move_line_count = self.env['stock.move'].search_count(domain)

    move_line_count = fields.Integer('Move lines', compute=_get_move_line_ids)


    def get_moves_domain(self):
        return [('purchase_id', '=', self.id), ('state', 'not in', DOMAIN_NOT_STATE)]

    @api.multi
    def _get_move_line_ids(self):
        for order in self.filtered(lambda x: x.procurement_group_id):
            domain = self.get_moves_domain()
            order.move_line_count = self.env['stock.move'].search_count(domain)

    @api.multi
    def action_view_move_lines(self):
        self.ensure_one()
        action = self.env.ref(
            'stock.stock_move_action').read()[0]
        action['domain'] = self.get_moves_domain()
        action['context'] = {'search_default_groupby_picking_type': True}
        return action

    @api.multi
    def action_cancel(self):
        ## Tengo que cancelar los movimientos sin albarnar
        domain = [('picking_id', '=', False), ('purchase_id', 'in', self.mapped('id'))]
        self.env['stock.move'].search(domain)._action_cancel()
        return super(PurchaseOrder, self).action_cancel()
