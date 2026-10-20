from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    allow_weekend_attendance = fields.Boolean(
        string='Allow weekend attendance',
        help='Allow this employee to register attendance on weekends.',
        copy=False,
    )
