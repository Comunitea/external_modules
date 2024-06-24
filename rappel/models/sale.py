# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    no_rappel = fields.Boolean("W/O Rappel", readonly=True,
                               states={'draft': [('readonly', False)]})


    def _prepare_invoice_line(self, **optional_values):
        vals = super()._prepare_invoice_line(**optional_values)
        vals['no_rappel'] = self.no_rappel
        return vals


    @api.onchange('product_id')
    def product_id_change(self):
        for record in self:
            if record.product_id and record.product_id.no_rappel:
                record.no_rappel = record.product_id.no_rappel
