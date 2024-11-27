from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_report_count = fields.Integer('Attendance Report Count', compute='_compute_attendance_report_count', readonly=True)

    def _compute_attendance_report_count(self):
        for employee in self:
            employee.attendance_report_count = self.env['hr.employee.attendance.report'].search_count([('employee_id', '=', employee.id)])
