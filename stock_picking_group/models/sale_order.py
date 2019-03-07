# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class ProcurementGroup(models.Model):

    _inherit = 'procurement.group'


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _action_launch_procurement_rule(self):
        self.filtered(lambda x: x.state == 'sale' and x.product_id.type in ('consum','product')).mapped('order_id').filtered(lambda x: not x.procurement_group_id).assign_group_procurement_value()
        return super()._action_launch_procurement_rule()

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id)
        values.update({
            'need_force_pick': self.order_id.need_force_pick,
        })

        return values

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def  _get_move_line_ids(self):
        for order in self:

            domain = [('picking_type_id.code', '=', 'outgoing'), ('state', '!=', 'cancel'), ('group_id', '=', order.procurement_group_id.id)]
            order.move_line_count = self.env['stock.move'].search_count(domain)

    need_force_pick = fields.Boolean('Picking auto', help='If checked, create picking when run procurement, (odoo default)', default=False)
    move_line_count = fields.Integer('Move lines', compute=_get_move_line_ids)


    def _prepare_proc_group_values(self):
        vals = {
            'name': self.name,
            'move_type': self.picking_policy,
            'sale_id': self.id,
            'partner_id': self.partner_shipping_id.id,
            'need_force_pick': self.need_force_pick
            }

        return vals

    @api.multi
    def assign_group_procurement_value(self):
        proc_obj = self.env['procurement.group']
        for order in self:
            vals = order._prepare_proc_group_values()
            order.procurement_group_id = proc_obj.create(vals)

    @api.multi
    def action_view_move_lines(self):
        self.ensure_one()

        action = self.env.ref(
            'stock.stock_move_action').read()[0]
        action['domain'] = [('picking_type_id.code', '=', 'outgoing'), ('state', '!=', 'cancel'), ('group_id', '=', self.procurement_group_id.id)]
        return action

        model_data = self.env['ir.model.data']
        #tree_view = model_data.get_object_reference(
        #    'stock_picking_group', 'sale_order_move_tree_view')


        #action['views'] = {
        #    (tree_view and tree_view[1] or False, 'tree')}






