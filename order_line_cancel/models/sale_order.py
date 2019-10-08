# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Comunitea All Rights Reserved
#    $Kiko Sánchez <kiko@comunitea.com>$
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

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_cancel(self):
        res = super().action_cancel()
        self.filtered(lambda x: x.state == 'sale').mapped('order_line').write({'cancel_state': 'ready'})
        return res

class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    cancel_state = fields.Selection([('ready', 'Ready'), ('cancel', 'Cancel')], string="Cancel state line", default='ready')

    @api.multi
    def action_cancel_line(self):
        for line in self:
            for move in line.move_ids:
                if move.state == 'done':
                    raise ValidationError (_("You have move in 'done' state"))
                move.action_cancel_move()
            line.cancel_state = 'cancel'

    @api.multi
    def action_re_order_line(self):
        for line in self.filtered(lambda x: x.cancel_state == 'cancel'):
            line._action_launch_procurement_rule()
            line.cancel_state = 'ready'