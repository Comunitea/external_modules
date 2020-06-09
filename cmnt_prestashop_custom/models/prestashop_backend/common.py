# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PrestashopBackend(models.Model):
    _inherit = "prestashop.backend"

    import_image_type = fields.Selection(
        [("url", "URL"), ("db", "Database")], default="url"
    )
    resize_images = fields.Boolean()
    start_import_date = fields.Datetime()
