# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, models, fields


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'

    default_code = fields.Char(related="product_id.default_code")
    barcode = fields.Char(related="product_id.barcode")
