import pytz

from odoo import SUPERUSER_ID, _, api, models
from odoo.exceptions import ValidationError


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.constrains('check_in', 'check_out')
    def _check_no_weekend(self):
        # env.user ignora sudo(): el fichaje de empleados se crea con sudo
        if (self.env.uid == SUPERUSER_ID or self.env.user.has_group(
                'hr_attendance.group_hr_attendance_manager')):
            return

        for att in self.filtered(
                lambda a: not a.employee_id.allow_weekend_attendance):
            tz = pytz.timezone(
                att.employee_id.tz or self.env.user.tz or 'UTC')
            for dt in (att.check_in, att.check_out):
                if dt and pytz.utc.localize(dt).astimezone(tz).weekday() >= 5:
                    raise ValidationError(_(
                        "Attendance on weekends is not allowed. Contact "
                        "HR to register this attendance."))
