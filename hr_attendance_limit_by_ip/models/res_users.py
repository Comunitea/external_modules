from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    allow_remote_check_in = fields.Boolean(
        string="Allow Remote Check-In",
        help="If enabled, the user will be able to check in remotely.",
        default=False,
    )
