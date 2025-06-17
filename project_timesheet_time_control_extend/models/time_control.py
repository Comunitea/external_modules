# © 2025 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, _


class HrTimesheetTimeControlMixin(models.AbstractModel):
    _inherit = "hr.timesheet.time_control.mixin"


    def button_end_work(self):
        if self.env.context.get("skip_stop_popup", False):
            return super().button_end_work()
        running_lines = self.env["account.analytic.line"].search(
            self._timesheet_running_domain(),
        )
        if not running_lines:
            return super().button_end_work()
        return {
            "name": _("Stop work"),
            "res_model": "hr.timesheet.stop.popup",
            "target": "new",
            "type": "ir.actions.act_window",
            "context": {
                "default_analytic_line_ids": running_lines.ids,
                "default_res_model": self._name,
                "default_res_id": self.id,

            },
            "view_mode": "form",
            "view_type": "form",
        }
