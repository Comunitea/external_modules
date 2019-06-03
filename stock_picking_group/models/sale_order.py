# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from .stock_move import DOMAIN_NOT_STATE

class ProcurementGroup(models.Model):

    _inherit = 'procurement.group'

    manual_pick = fields.Boolean('Manual Picking', help='If checked, no create pickings when confirm order', default=True)

    @api.model
    def create(self, vals):
        if vals.get('sale_id', False):
            sale = self.env['sale.order'].browse(vals.get('sale_id', False))
            vals.update(manual_pick=sale.manual_pick)
        return super().create(vals)

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _action_launch_procurement_rule(self):
        return super()._action_launch_procurement_rule()

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id)
        values.update({
            'manual_pick': self.order_id.manual_pick,
            'sale_id': self.order_id.id,
            'shipping_id': self.order_id.partner_shipping_id.id
            })
        return values

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _compute_picking_ids(self):
        for sale in self:
            sale.picking_ids = self.env["stock.move"].search(sale.get_moves_domain()).mapped('picking_id')
            sale.delivery_count = len(sale.picking_ids)

    def get_moves_domain(self):
        return [('sale_id', '=', self.id), ('state', 'not in', DOMAIN_NOT_STATE)]

    @api.multi
    def _get_move_line_ids(self):
        for order in self.filtered(lambda x: x.procurement_group_id):
            domain = self.get_moves_domain()
            order.move_line_count = self.env['stock.move'].search_count(domain)

    manual_pick = fields.Boolean('Manual Picking', help='If checked, no create pickings when confirm order', default=True)
    move_line_count = fields.Integer('Move lines', compute=_get_move_line_ids)
    picking_ids = fields.One2many('stock.picking', compute="_compute_picking_ids", string='Pickings')

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
        ctx = self._context.copy()
        for order in self:
            ctx.update(cancel_from_sale=order.id)
            super(SaleOrder, order.with_context(ctx)).action_cancel()

        domain = [('picking_id', '=', False), ('sale_id', 'in', self.mapped('id'))]
        self.env['stock.move'].search(domain)._action_cancel()