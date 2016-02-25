# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Comunitea Servicios Tecnológicos S.L.
#    $Omar Castiñeira Saavedra$
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, _, api, exceptions


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.one
    def _get_picking_ids(self):
        line_ids = [x.id for x in self.order_line]
        moves = self.env['stock.move'].\
            search([('procurement_id.sale_line_id', 'in', line_ids)])
        picking_ids = [x.picking_id.id for x in moves if x.picking_id]
        self.picking_ids = list(set(picking_ids))

    no_picking = fields.Boolean('No picking', default=True)
    picking_ids = fields.One2many("stock.picking", compute="_get_picking_ids",
                                  string='Picking associated to this sale')


class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.multi
    def action_undo(self):
        for pick in self:
            for move in pick.move_lines:
                move.picking_id = False
            pick.unlink()

        action = {}
        try:
            action = self.env.ref('no_pickings.action_move_form_no_picking')
        except ValueError:
            raise exceptions.\
                Warning(_('Error'),
                        _('Object reference %s not found'
                            % 'action_move_form_no_picking'))

        action = action.read()
        return action


class StockMove(models.Model):

    _inherit = "stock.move"

    @api.multi
    def _picking_assign(self, procurement_group, location_from, location_to):
        if procurement_group:
            sales = self.env['sale.order'].search([('procurement_group_id',
                                                    '=', procurement_group)])
            if sales:
                if sales[0].no_picking:
                    return False
        return super(StockMove, self)._picking_assign(procurement_group,
                                                      location_from,
                                                      location_to)
