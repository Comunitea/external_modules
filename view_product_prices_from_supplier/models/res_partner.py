# -*- coding: utf-8 -*-
# Copyright 2019 Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    product_prices_count = fields.Integer('# Products',
                                          compute='_count_product_prices')

    @api.multi
    def _count_product_prices(self):
        for partner in self:
            domain = [('name', '=', partner.id)]
            count = self.env['product.supplierinfo'].search_count(domain)
            partner.product_prices_count = count
