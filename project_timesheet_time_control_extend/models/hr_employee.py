# © 2025 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _attendance_action_change(self):
        if self.attendance_state == 'checked_in':
            # If the employee is checked in, we stop the currents running timesheets
            task_ids = self.env['account.analytic.line'].search([
                ('employee_id', '=', self.id),
            ]).mapped('task_id').filtered(lambda x: x.show_time_control == "stop")

            task_ids.with_context(skip_stop_popup=True).button_end_work()

        return super()._attendance_action_change()
