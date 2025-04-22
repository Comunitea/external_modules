##############################################################################
#
#    Copyright (C) 2025 Comunitea All Rights Reserved
#    $Miguel Granda Martínez <mgranda@comunitea.com>$
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class HrAttendanceReport(models.AbstractModel):
    _name = "report.hr_attendance_report.print_attendance"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        employee_attendance = {}
        totals = {}
        for employee in self.env["hr.employee"].browse(data["ids"]):

            contracts = self.env["hr.contract"].search([
                ("employee_id", "=", employee.id),
                ("state", "!=", "draft"),
                ("state", "!=", "cancel"),
            ])
            if not contracts and self.env["hr.attendance"].search([
                ("employee_id", "=", employee.id)
            ]) is not False:
                data["ids"].remove(employee.id)
                continue
            employee_attendance[employee.id] = []
            docs.append(employee)
            from_date_s = data.get("form", {}).get("from_date", "")
            to_date_s = data.get("form", {}).get("to_date", "")
            from_date = datetime.strptime(from_date_s, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date_s, "%Y-%m-%d").date()

            while from_date <= to_date:
                from_date_1 = datetime.strftime(from_date, "%Y-%m-%d %H:%M:%S")
                from_date_datetime = datetime.strptime(
                    from_date_1, "%Y-%m-%d %H:%M:%S"
                )
                from_date_2 = datetime.strftime(from_date, "%Y-%m-%d 23:59:59")
                attendances = self.env["hr.attendance"].search([
                    ("employee_id", "=", employee.id),
                    ("check_in", ">=", from_date_1),
                    ("check_in", "<=", from_date_2),
                    ("check_out", "!=", False),
                ], order="check_in asc")
                if contracts:
                    date_in_contract = False
                    for contract in contracts:
                        if from_date_datetime.date() >= contract.date_start and \
                                (not contract.date_end or from_date_datetime.date() <= contract.date_end):
                            date_in_contract = True
                            break
                    if not date_in_contract:
                        from_date += relativedelta(days=1)
                        continue
                day_attendances = {
                    "ord_hours": 0,
                    "extra": 0,
                    "in_out_str": "",
                    "day": from_date_1[8:10],
                }
                used_ids = []
                for attendance in attendances:

                    in_time = fields.Datetime.context_timestamp(
                        self, attendance.check_in,
                    )
                    out_time = fields.Datetime.context_timestamp(
                        self, attendance.check_out,
                    )
                    day_attendances["ord_hours"] += attendance.worked_hours

                    fields.Datetime.context_timestamp(
                        self, attendances[0].check_in
                    )
                    day_attendances["in_out_str"] += "%02d:%02d-%02d:%02d | " % (
                        in_time.hour,
                        in_time.minute,
                        out_time.hour,
                        out_time.minute,
                    )

                    used_ids.append(attendance.id)
                    used_ids.append(attendance.id)
                if employee.resource_calendar_id and \
                        employee.resource_calendar_id.attendance_ids:
                    from_date2_datetime = datetime.strptime(
                        from_date_2, "%Y-%m-%d %H:%M:%S"
                    )
                    # max_hours = employee.resource_calendar_id.get_work_hours_count(
                    #     from_date_datetime,
                    #     from_date2_datetime,
                    # )
                    # Corrijo que no se tienen en cuenta ni los hr.leaves
                    # específicos de empleado ni los festivos de OCA
                    max_hours = employee.resource_calendar_id.get_work_hours_count_exclude_all(
                        from_date_datetime,
                        from_date2_datetime,
                        employee
                    )
                    extra_hours = day_attendances["ord_hours"] - max_hours
                    if day_attendances["ord_hours"] > max_hours:
                        day_attendances["ord_hours"] = max_hours
                    day_attendances["extra"] += extra_hours
                if day_attendances["in_out_str"]:
                    day_attendances["in_out_str"] = day_attendances[
                        "in_out_str"
                    ][:-3]
                if day_attendances["ord_hours"] or day_attendances["extra"]:
                    employee_attendance[employee.id].append(day_attendances)
                from_date += relativedelta(days=1)

            overtime = self.env["hr.attendance.overtime"].sudo().search(
                [
                    ("employee_id", "=", employee.id),
                    ("date", ">=", datetime.strptime(from_date_s, "%Y-%m-%d").date()),
                    ("date", "<=", datetime.strptime(to_date_s, "%Y-%m-%d").date()),
                ]
            )

            extra = 0.0
            if overtime:
                extra = sum(
                    duration for duration in overtime.mapped("duration")
                )
            else:
                extra = sum(
                    x["extra"] for x in employee_attendance[employee.id]
                )

            totals[employee.id] = {
                "total": sum(
                    x["ord_hours"] for x in employee_attendance[employee.id]
                )
                + sum(x["extra"] for x in employee_attendance[employee.id]),
                "ordinary": sum(
                    x["ord_hours"] for x in employee_attendance[employee.id]
                ),
                "complementary": 0,
                "extra": extra
            }
        docargs = {
            "doc_ids": data["ids"],
            "doc_model": "hr.employee",
            "docs": docs,
            "attendances": employee_attendance,
            "data": data,
            "totals": totals,
        }
        return docargs
