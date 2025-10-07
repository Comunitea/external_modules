from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ips_allowed_for_check_in = fields.Text(
        related='company_id.ips_allowed_for_check_in',
        readonly=False,
        string="IPs allowed for check in/out",
        help="List of IPs or IP ranges allowed for employees to check in/out. One per line. Need to be a regular expression.",
    )
