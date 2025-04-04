# © 2023 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ResCompany(models.Model):

    _inherit = "res.company"

    show_backend_logo = fields.Boolean('Show company logo in backend')
