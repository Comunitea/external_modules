# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    no_rappel = fields.Boolean("W/O Rappel", readonly=True,
                               states={'draft': [('readonly', False)]})

    @api.model
    def _prepare_invoice_line(self, qty):
        vals = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        vals['no_rappel'] = self.no_rappel
        return vals
