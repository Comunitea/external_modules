from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    attendance_report_autocreation_period = fields.Selection(
        related='company_id.attendance_report_autocreation_period',
        readonly=False
    )
    company_partner_to_send_id = fields.Many2one(
        related='company_id.partner_to_send_id',
        readonly=False
    )
    partner_to_send_id = fields.Many2one(
        'res.partner',
        relation="hr_attendance_report_portal_partner_config",
        config_parameter="hr_attendance_report_portal.partner_to_send_id",
        domain="[('company_id', '=', False)]",
    )
