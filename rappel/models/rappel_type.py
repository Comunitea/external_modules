# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class RappelType(models.Model):

    _name = 'rappel.type'
    _description = 'Rappel Type Model'

    name = fields.Char(size=255, required=True)
    code = fields.Char(size=56)
    product_id = fields.Many2one("product.product", "Rappel product",
                                 required=True, help="Product used to invoice"
                                                     " rappels this type.")
