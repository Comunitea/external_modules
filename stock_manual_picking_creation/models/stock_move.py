# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, 
                               location_id, name, origin, values, group_id):
        """
        Adds manual_pick fields to the move from the related sale
        """
        vals = super()._get_stock_move_values(product_id=product_id,
                                              product_qty=product_qty,
                                              product_uom=product_uom,
                                              location_id=location_id,
                                              name=name,
                                              origin=origin,
                                              values=values,
                                              group_id=group_id)
        
        if group_id:
            group = self.env['procurement.group'].browse(group_id)
            vals.update(manual_pick=
                group.sale_id.manual_pick)
        vals.update({
            'sale_price': values.get('sale_price'),
            'sale_id': values.get('sale_id'),
            'shipping_id': values.get('shipping_id'),
        })
        return vals


class StockMove(models.Model):

    _inherit = "stock.move"

    manual_pick = fields.Boolean(
        'Manual Picking',
        help='If checked, no create pickings when confirm order',
        default=False, copy=True)
    sale_id = fields.Many2one(
        'sale.order', 'Saler Order')
    sale_price = fields.Float('Sale Price')
    shipping_id = fields.Many2one('res.partner', string='Delivery Address')
    

    def _assign_picking(self):
        """
        Avoid picking creation if is marked to Manual it
        """
        if self.manual_pick:
            self._action_assign()
            return

        super()._assign_picking()
        for move in self:
            move.move_line_ids.write({'picking_id': move.picking_id.id})


    @api.multi
    def action_force_assign_picking(self, manual_pick=False):
        """
        Button method. Create picking
        """
        self.write({'manual_pick': False})
        return self._assign_picking()
    
    def _prepare_procurement_values(self):
        """ 
        Pass move custom fields to the linked move
        """
        vals = super()._prepare_procurement_values()
        vals.update({
            'sale_id': self.sale_id.id,
            'sale_price': self.sale_price,
            'shipping_id': self.shipping_id.id
        })
        return vals

