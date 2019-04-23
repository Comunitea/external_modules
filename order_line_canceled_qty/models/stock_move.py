# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp

class StockMove(models.Model):

    _inherit = 'stock.move'

    def _action_cancel(self):
        super()._action_cancel()
        self.mapped('sale_line_id')._get_cancelled_qty()
        self.mapped('purchase_line_id')._get_cancelled_qty()
        return True