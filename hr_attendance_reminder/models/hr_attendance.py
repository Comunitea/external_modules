# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api
from datetime import datetime
from datetime import timedelta


class HrAttendance(models.Model):

    _inherit = 'hr.attendance'

    def get_nearest_interval(self, intervals):
        closest_time = False
        closest_interval = False
        for interval in intervals:
            if interval[1] > datetime.now():
                raise Exception()
            if not closest_time or (datetime.now() - interval[1]).seconds \
                    < closest_time:
                closest_time = (datetime.now() - interval[1]).seconds < \
                    closest_time
                closest_interval = interval
        return closest_interval

    @api.model
    def cron_attendance_reminder(self):
        for employee in self.env['hr.employee'].search(
                [('calendar_id', '!=', False)]):
            currently_working = employee.attendance_state == 'checked_in' and True or False
            calendar = employee.calendar_id
            intervals = calendar.get_working_intervals_of_day(
                compute_leaves=True, resource_id=employee.resource_id.id)
            if currently_working:
                try:
                    nearest_interval = self.get_nearest_interval(intervals)
                except Exception:
                    # Aun está en su horario por lo que pasamos al siguiente.
                    continue
                if (datetime.now() - nearest_interval[1]).seconds \
                        / 60.0 / 60.0 > 1:
                    # Aunque ya se haya pasado el momento de salida,
                    # si ya ha pasado mas de 1 hora no se envia,
                    # para evitar el envio continuo de emails.
                    continue
                self.env.ref('hr_attendance_reminder.email_template_attendance_reminder').send_mail(employee.id)
            else:
                for interval in intervals:
                    if interval[1] < datetime.now() or \
                                interval[0] > datetime.now():
                        continue
                    if interval[0] < datetime.now() + \
                            timedelta(minutes=-calendar.reminder_delay) and \
                            (datetime.now() - interval[0]).seconds\
                            / 60.0 / 60.0 < 1:
                        self.env.ref('hr_attendance_reminder.email_template_attendance_reminder').send_mail(employee.id)
                        break
