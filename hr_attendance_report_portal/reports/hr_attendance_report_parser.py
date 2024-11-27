from odoo import models, api
from dateutil.relativedelta import relativedelta
from datetime import datetime


class EmployeePrintAttendanceReport(models.AbstractModel):
    _inherit = 'report.hr_attendance_report.print_attendance'

    @api.model
    def _get_report_values(self, docids, data=None):
        res = super(EmployeePrintAttendanceReport, self)._get_report_values(docids, data)

        from_date = datetime.strptime(data['form']['from_date'], '%Y-%m-%d').date()
        to_date = datetime.strptime(data['form']['to_date'], '%Y-%m-%d').date()
        attendance_report = data['form'].get('attendance_report', False)
        if attendance_report:
            attendance_report = self.env['hr.employee.attendance.report'].browse(attendance_report)

        for employee in res['docs']:
            num_months = (to_date.year - from_date.year) * 12 + to_date.month - from_date.month
            month_attendance = {}
            # Si hay más de un mes separamos las asistencias por mes para poder ordenarlas
            if num_months > 0:
                last_day = 0
                month = 0
                month_attendance[month] = []
                for attendance in res['attendances'][employee.id]:
                    if int(attendance['day']) < last_day:
                        month += 1
                        month_attendance[month] = []
                    month_attendance[month].append(attendance)
                    last_day = int(attendance['day'])
            # Buscar las fechas de vacaciones y faltas de asistencia del empleado
            leaves = self.env['hr.leave'].search([
                ('employee_id', '=', employee.id),
                ('date_from', '>=', from_date),
                ('date_to', '<=', to_date),
                '|',
                ('state', '=', 'validate'),
                ('state', '=', 'validate1'),
            ])
            for leave in leaves:
                date = leave.date_from
                while date <= leave.date_to:
                    if num_months > 0:
                        month = (date.year - from_date.year) * 12 + date.month - from_date.month
                        month_attendance[month].append({
                            'day': str(date.day),
                            'extra': 0,
                            'ord_hours': 0,
                            'in_out_str': leave.holiday_status_id.name
                        })
                    else:
                        res['attendances'][employee.id].append({
                            'day': str(date.day),
                            'extra': 0,
                            'ord_hours': 0,
                            'in_out_str': leave.holiday_status_id.name
                        })
                    date += relativedelta(days=1)
            # Buscar los festivos
            holidays = self.env['hr.holidays.public'].get_holidays_list(
                start_dt=from_date,
                end_dt=to_date,
                partner_id=employee.user_id.partner_id.id
            )
            for holiday in holidays:
                if num_months > 0:
                    month = (holiday.date.year - from_date.year) * 12 + holiday.date.month - from_date.month
                    month_attendance[month].append({
                        'day': str(holiday.date.day),
                        'extra': 0,
                        'ord_hours': 0,
                        'in_out_str': holiday.name
                    })
                else:
                    res['attendances'][employee.id].append({
                        'day': str(holiday.date.day),
                        'extra': 0,
                        'ord_hours': 0,
                        'in_out_str': holiday.name
                    })
            # reordenamos las asistencias por día
            if num_months > 0:
                del res['attendances'][employee.id][:]
                res['attendances'][employee.id] = []
                for month in month_attendance:
                    for attendance in sorted(month_attendance[month], key=lambda k: k['day']):
                        res['attendances'][employee.id].append(attendance)
            else:
                res['attendances'][employee.id] = sorted(res['attendances'][employee.id], key=lambda k: k['day'])

            if attendance_report:
                res['signature'] = "data:image/png;base64, %s" % str(attendance_report.signature)[2:-1]
            else:
                res['signature'] = False

        return res
