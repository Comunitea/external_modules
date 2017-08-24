# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api

class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.model
    def _create_invoice_from_picking(self, picking, vals):
        if picking and picking.sale_id and picking.sale_id.early_payment_discount:
            vals['early_payment_discount'] = picking.sale_id.early_payment_discount

        return super(StockPicking, self)._create_invoice_from_picking(picking, vals)
