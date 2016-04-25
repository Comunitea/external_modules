# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, exceptions, _


class SaleOrder(models.Model):

    _inherit = "sale.order"

    valued_picking = fields.Boolean('Valued picking', help="If it sets to True, the picking will be valued", readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def action_ship_create(self):
        res = super(SaleOrder, self).action_ship_create()
        for order in self:
            order.picking_ids.write({'valued_picking': order.valued_picking})
        return res

    @api.multi
    def onchange_partner_id(self, part):
        res = super(SaleOrder, self).onchange_partner_id(part)
        if not part:
            res['value']['valued_picking'] = False
            return res
        partner_obj = self.env['res.partner'].browse(part)
        res['value']['valued_picking'] = partner_obj.valued_picking
        return res
