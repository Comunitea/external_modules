from odoo import models


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    def print_attendance_report(self):

        return self.env["ir.actions.actions"]._for_xml_id('hr_attendance_report.hr_employee_public_print_assitance_report_action')
