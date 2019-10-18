# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    diff_level = fields.Integer('Template diff level', default=1, help="Template diff level")



