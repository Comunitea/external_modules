from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    ips_allowed_for_check_in = fields.Text(
        string="IPs allowed for check in/out",
        help="List of IPs or IP ranges allowed for employees to check in/out. One per line. Need to be a regular expression.",
    )
