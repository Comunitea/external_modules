# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    route_id = fields.Many2one('stock.location.route', string='Route', domain=[('sale_selectable', '=', True)],
                               ondelete='restrict')

    @api.multi
    def apply_route_id(self):
        for order in self:
            route_id = self.route_id and self.route_id.id or False
            order.order_line.write({'route_id': route_id})