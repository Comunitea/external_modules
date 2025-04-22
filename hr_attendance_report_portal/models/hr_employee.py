from odoo import models, fields
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_report_count = fields.Integer('Attendance Report Count', compute='_compute_attendance_report_count', readonly=True)

    def _compute_attendance_report_count(self):
        for employee in self:
            employee.attendance_report_count = self.env['hr.employee.attendance.report'].search_count([('employee_id', '=', employee.id)])

    def _create_attendance_report(self, automatic=False, use_new_cursor=False):
        today = fields.Date.today()
        for company in self.env['res.company'].search([]):
            if company.attendance_report_autocreation_period == 'monthly':
                from_date = today.replace(day=1) - relativedelta(months=1)
                to_date = from_date + relativedelta(months=1, days=-1)
            elif company.attendance_report_autocreation_period == 'bimonthly':
                from_date = today.replace(day=1, month=((today.month - 1) // 2) * 2 + 1) - relativedelta(months=2)
                to_date = from_date + relativedelta(months=2, days=-1)
            elif company.attendance_report_autocreation_period == 'quarterly':
                from_date = today.replace(day=1, month=((today.month - 1) // 3) * 3 + 1) - relativedelta(months=3)
                to_date = from_date + relativedelta(months=3, days=-1)
            elif company.attendance_report_autocreation_period == 'yearly':
                from_date = today.replace(day=1, month=1) - relativedelta(years=1)
                to_date = from_date + relativedelta(years=1, days=-1)

            reports = self.env['hr.employee.attendance.report'].search([
                ('from_date', '<=', to_date),
                ('to_date', '>=', to_date),
                ('company_id', '=', company.id),
            ]) + self.env['hr.employee.attendance.report'].search([
                ('from_date', '<=', from_date),
                ('to_date', '>=', from_date),
                ('company_id', '=', company.id),
            ]) + self.env['hr.employee.attendance.report'].search([
                ('from_date', '>', from_date),
                ('to_date', '<', to_date),
                ('company_id', '=', company.id),
            ])

            employee_ids = self.env['hr.employee'].search([
                ('id', 'not in', reports.mapped('employee_id').ids),
                ('active', '=', True),
                ('company_id', '=', company.id),
            ])

            if employee_ids:
                vals = []

                for employee in employee_ids:
                    lines = self.env['hr.employee.attendance.report'].get_lines(employee, from_date, to_date)
                    if lines != []:
                        vals.append({
                            'employee_id': employee.id,
                            'from_date': from_date,
                            'to_date': to_date,
                        })
                self.env['hr.employee.attendance.report'].create(vals)
