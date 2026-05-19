# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    no_rappel = fields.Boolean("W/O Rappel")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and self.product_id.no_rappel:
            self.no_rappel = self.product_id.no_rappel
