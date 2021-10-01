##############################################################################
#
#    Copyright (C) 2004-TODAY
#    Comunitea Servicios Tecnológicos S.L. (https://www.comunitea.com)
#    All Rights Reserved
#    $Kiko Sánchez
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    
    def get_moves_search_domain(self):
        return {
            'search_default_groupby_picking_type': True,
            'search_default_future': True,
            'hide_reference': True,
            'hide_product': True,
            'hide_picking': False,
        }
    @api.multi
    def action_open_list_stock_moves(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id.product_tmpl_id', 'in', self.ids)]
        context = self._context.copy()
        context.update (self.get_moves_search_domain())
        action['context']= context

        return action

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def action_open_list_stock_moves(self):

        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id', 'in', self.ids)]
        context = self._context.copy()
        context.update(self.env['product.template'].get_moves_search_domain())
        action['context']= context

        return action