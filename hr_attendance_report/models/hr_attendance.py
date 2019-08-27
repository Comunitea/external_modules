# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields
from datetime import datetime


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    def _compute_worked_hours(self):
        """
            Override the function to remove store and prevent rounding problems
        """
        for attendance in self:
            if attendance.action == 'sign_in':
                attendance.worked_hours = 0
            elif attendance.action == 'sign_out':
                # Get the associated sign-in
                last_signin = self.search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('name', '<', attendance.name), ('action', '=', 'sign_in')
                ], limit=1, order='name DESC')
                if last_signin:
                    # Compute time elapsed between sign-in and sign-out
                    last_signin_datetime = datetime.strptime(
                        last_signin.name[:-3], '%Y-%m-%d %H:%M')
                    signout_datetime = datetime.strptime(
                        attendance.name[:-3], '%Y-%m-%d %H:%M')
                    workedhours_datetime = (
                        signout_datetime - last_signin_datetime)
                    attendance.worked_hours = (
                        (workedhours_datetime.total_seconds()) / 60) / 60.0
                else:
                    attendance.worked_hours = False

    worked_hours = fields.Float(compute='_compute_worked_hours', store=False)
