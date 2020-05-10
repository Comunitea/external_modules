# -*- coding: utf-8 -*-


from odoo import api, models, fields

class StockWarehouse(models.Model):

    _inherit = 'stock.warehouse'
    barcode_re = fields.Char("E. Regular", help="Expresión regular para que la pistola detecte una ubicación",
                             default="/\d{3}[-\/\.]\d{3}[-\/\.]\d{2}\b/")