from odoo import models, fields, _
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
            for employee in employee_ids:
                if not reports:
                    report = self.env['hr.employee.attendance.report'].create({
                        'employee_id': employee.id,
                        'from_date': from_date,
                        'to_date': to_date,
                    })

                    report.message_unsubscribe(partner_ids=report.message_follower_ids.mapped('partner_id').ids)
                    report.message_subscribe(partner_ids=report.employee_id.user_id.partner_id.ids)

                    report.message_post(
                        body=_('%s attendance report has been created, please sign it <a href="%s">here<a>') % (report.name, report.access_url),
                        subject=_('Attendance Report Created'),
                        attachment_ids=[],
                        message_type="email",
                        subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment'),
                    )

                    report._compute_message_follower_ids()
