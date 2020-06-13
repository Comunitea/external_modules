# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ProductTemplate(models.Model):

    _inherit = "product.template"

    no_rappel = fields.Boolean("Without rappel")
