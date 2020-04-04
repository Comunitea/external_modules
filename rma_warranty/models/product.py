# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    warranty_duration = fields.Integer(
        "Warranty duration (in days)", default=730
    )
