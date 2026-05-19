# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    no_rappel = fields.Boolean("W/O Rappel")


    def _prepare_invoice_line(self, **optional_values):
        vals = super()._prepare_invoice_line(**optional_values)
        vals['no_rappel'] = self.no_rappel
        return vals


    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        if self.product_id and self.product_id.no_rappel:
            self.no_rappel = self.product_id.no_rappel
        return res
