# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, exceptions, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class HrAttendanceReport(models.AbstractModel):
    _name = 'report.hr_attendance_report.print_attendance'

    @api.multi
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'hr_attendance_report.print_attendance')
        docs = []
        employee_attendance = {}
        totals = {}
        for employee in self.env[report.model].browse(data['ids']):
            employee_attendance[employee.id] = []
            docs.append(employee)
            from_date_s = data.get('form', {}).get('from_date', '')
            to_date_s = data.get('form', {}).get('to_date', '')
            from_date = datetime.strptime(from_date_s, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_s, '%Y-%m-%d').date()
            while from_date <= to_date:
                from_date_1 = datetime.strftime(from_date, "%Y-%m-%d %H:%M:%S")
                from_date_datetime = datetime.strptime(from_date_1, '%Y-%m-%d %H:%M:%S')
                from_date_2 = datetime.strftime(from_date, "%Y-%m-%d 23:59:59")
                attendances = self.env['hr.attendance'].search(
                    [('employee_id', '=', employee.id),
                     ('check_in', '>=', from_date_1),
                     ('check_in', '<=', from_date_2),
                     ('check_out', '!=', False)], order='check_in asc')
                day_attendances = {'ord_hours': 0, 'extra': 0, 'in_out_str': '',
                                   'day': from_date_1[8:10]}
                used_ids = []
                for attendance in attendances:

                    in_time = fields.Datetime.context_timestamp(
                        self, datetime.strptime(attendance.check_in,
                                                "%Y-%m-%d %H:%M:%S"))
                    out_time = fields.Datetime.context_timestamp(
                        self, datetime.strptime(attendance.check_out,
                                                "%Y-%m-%d %H:%M:%S"))
                    day_attendances['ord_hours'] += attendance.worked_hours

                    fields.Datetime.context_timestamp(
                        self, datetime.strptime(attendances[0].check_in,
                                                "%Y-%m-%d %H:%M:%S"))
                    day_attendances['in_out_str'] += \
                        '%02d:%02d-%02d:%02d | ' % (in_time.hour,
                                                    in_time.minute,
                                                    out_time.hour,
                                                    out_time.minute)
                    used_ids.append(attendance.id)
                    used_ids.append(attendance.id)
                if employee.calendar_id:
                    max_hours = employee.calendar_id.get_working_hours_of_date(from_date_datetime, resource_id=employee.resource_id.id)
                    extra_hours = day_attendances['ord_hours'] - max_hours
                    if day_attendances['ord_hours'] > max_hours:
                        day_attendances['ord_hours'] = max_hours
                    day_attendances['extra'] += extra_hours
                if day_attendances['in_out_str']:
                    day_attendances['in_out_str'] = \
                        day_attendances['in_out_str'][:-3]
                if day_attendances['ord_hours'] or day_attendances['extra']:
                    employee_attendance[employee.id].append(day_attendances)
                from_date += relativedelta(days=1)
            totals[employee.id] = {
                'total': sum(x['ord_hours'] for x in
                             employee_attendance[employee.id]) + sum(x['extra'] for x in
                             employee_attendance[employee.id]),
                'ordinary': sum(x['ord_hours'] for x in
                                employee_attendance[employee.id]),
                'complementary': 0,
                'extra': sum(x['extra'] for x in
                                employee_attendance[employee.id])
            }
        docargs = {
            'doc_ids': data['ids'],
            'doc_model': report.model,
            'docs': docs,
            'attendances': employee_attendance,
            'data': data,
            'totals': totals
        }
        return report_obj.render('hr_attendance_report.print_attendance',
docargs)
