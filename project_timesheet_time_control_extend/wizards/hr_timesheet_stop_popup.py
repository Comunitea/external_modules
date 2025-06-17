# © 2025 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class HrTimesheetSwitch(models.TransientModel):
    _name = "hr.timesheet.stop.popup"
    _description = "Set a new description before stopping the timer"

    analytic_line_ids = fields.Many2many(
        comodel_name="account.analytic.line", string="Origin line"
    )
    name = fields.Char(string="Description", required=True)
    res_model = fields.Char(
        string="Related model",
        required=True,
        help="Model where the timesheet line is related to.",
    )
    res_id = fields.Integer(
        string="Related record",
        required=True,
        help="Record where the timesheet line is related to.",
    )

    def action_save(self):
        """Stop the running timer and set a new description."""
        if not self.analytic_line_ids:
            raise UserError(_("No running timesheet lines found."))

        # Update the description of the stopped lines
        self.analytic_line_ids.write({"name": self.name})

        record = self.env[self.res_model].browse(self.res_id)
        if not record:
            raise UserError(_("The related record does not exist."))

        record.with_context(skip_stop_popup=True).button_end_work()
