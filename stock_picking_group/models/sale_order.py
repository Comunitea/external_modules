# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

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

    def get_moves_domain(self):
        return [('picking_type_id.code', '=', 'outgoing'), ('sale_id', '=', self.id)]

    @api.multi
    def _get_move_line_ids(self):
        for order in self.filtered(lambda x: x.procurement_group_id):
            domain = self.get_moves_domain()
            order.move_line_count = self.env['stock.move'].search_count(domain)

    manual_pick = fields.Boolean('Manual Picking', help='If checked, no create pickings when confirm order', default=True)
    move_line_count = fields.Integer('Move lines', compute=_get_move_line_ids)

    @api.multi
    def action_view_move_lines(self):
        self.ensure_one()
        action = self.env.ref(
            'stock.stock_move_action').read()[0]
        action['domain'] = self.get_moves_domain()
        action['context'] = {'search_default_groupby_location_id': True}
        return action

    @api.multi
    def action_cancel(self):
        ## Tengo que cancelar los movimientos sin albarnar
        domain = [('picking_id', '=', False), ('sale_id', 'in', self.mapped('id'))]
        self.env['stock.move'].search(domain)._action_cancel()
        return super(SaleOrder, self).action_cancel()
