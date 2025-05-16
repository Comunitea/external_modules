# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api
from datetime import datetime
from datetime import timedelta
from pytz import utc


class HrAttendance(models.Model):

    _inherit = 'hr.attendance'

    def get_nearest_interval(self, intervals, employee):
        closest_time = False
        closest_interval = False
        for interval in intervals:
            # date_now = utc.localize(datetime.now())
            date_now = datetime.now()
            if interval[1] > date_now:
                return False
            if not closest_time or (date_now - interval[1]).seconds \
                    < closest_time:
                closest_time = (date_now - interval[1]).seconds < \
                    closest_time
                closest_interval = interval
        if not closest_interval:
            raise Exception(
                'Interval not found for employee %s' % employee.name)
        return closest_interval

    @api.model
    def cron_attendance_reminder(self):
        for employee in self.env['hr.employee'].search([('resource_calendar_id', '!=', False)]):
            currently_working = employee.attendance_state == 'checked_in' and True or False
            calendar = employee.resource_calendar_id

            start_today = utc.localize(datetime.now().replace(hour=0, minute=0, second=0))
            end_today = utc.localize(datetime.now().replace(hour=23, minute=59, second=59))

            # Necesario para excluir los festivos de OCA, y el employee_id para
            # que lo haga por provincias también
            self = self.with_context(
                exclude_public_holidays=True, employee_id=employee.id)
            holiday_intervals = employee.resource_calendar_id._attendance_intervals_batch(
                start_today, end_today, employee.resource_id)[employee.resource_id.id]
            hours_without_holidays = sum(
                (stop - start).total_seconds() / 3600
                for start, stop, meta in holiday_intervals
            )
            # Era festivo, devuelvo 0
            if not hours_without_holidays:
                continue
                
            # Para que odoo descuente las ausencias necesito pasarle el recurso del empleado
            intervals_batch = employee.resource_calendar_id._work_intervals_batch(
                start_today, end_today, resources=employee.resource_id)
            intervals_data = intervals_batch[employee.resource_id.id]
            intervals = []

            # Convierto a lista de intervalos como en v10
            if intervals_data: 
                intervals = [(start.replace(tzinfo=None), stop.replace(tzinfo=None)) for start, stop, records in intervals_data]  # Convert intervals in interval list

            if currently_working:
                if intervals:
                    nearest_interval = self.get_nearest_interval(
                        intervals, employee)
                    if not nearest_interval:
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
