# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    no_rappel = fields.Boolean("W/O Rappel")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for record in self:
            if record.product_id and record.product_id.no_rappel:
                record.no_rappel = record.product_id.no_rappel
