from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    attendance_report_autocreation_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('bimonthly', 'Bimonthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Period', default='monthly', required=True)

    partner_to_send_id = fields.Many2one(
        'res.partner',
        string='Partner to Send',
        relation="hr_attendance_report_portal_partner_company",
        domain="[('company_id', '=', id)]",
    )
