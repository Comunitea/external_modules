# © 2026 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
from datetime import date, datetime

from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAttendanceReport(TransactionCase):
    """Informe de registro de jornada: horas teóricas, horas extra, asistente y PDF.

    Todo en UTC (calendario, empleado y contexto) para que las horas del test sean las
    del horario. Semana del lunes 2026-11-16: de 08:00 a 12:00 y de 13:00 a 17:00 (8 h).
    El miércoles 2026-11-18 es festivo (OCA) para el país del empleado.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tz="UTC"))
        cls.calendar = cls.env["resource.calendar"].create(
            {
                "name": "Horario test informe",
                "tz": "UTC",
                "attendance_ids": [
                    (0, 0, {"name": f"{day} {start}", "dayofweek": str(day),
                            "hour_from": start, "hour_to": end})
                    for day in range(5)
                    for start, end in ((8, 12), (13, 17))
                ],
            }
        )
        cls.country = cls.env.ref("base.ad")
        cls.address = cls.env["res.partner"].create(
            {"name": "Centro de trabajo test", "country_id": cls.country.id,
             "vat": "AD123456X", "street": "Rúa test 1", "city": "Andorra"}
        )
        cls.user = cls.env["res.users"].create(
            {"name": "Empleado informe", "login": "attendance_report_test",
             "email": "attendance_report@example.com", "tz": "UTC",
             "group_ids": [(6, 0, [cls.env.ref("base.group_user").id])]}
        )
        cls.employee = cls.env["hr.employee"].create(
            {"name": "Empleado informe", "user_id": cls.user.id,
             "resource_calendar_id": cls.calendar.id, "tz": "UTC",
             "address_id": cls.address.id}
        )
        cls.env["calendar.public.holiday"].create(
            {"year": 2026, "country_id": cls.country.id,
             "line_ids": [(0, 0, {"name": "Festivo test", "date": "2026-11-18"})]}
        )
        cls.Report = cls.env["report.hr_attendance_report.print_attendance"]

    def _hours(self, day):
        return self.calendar.get_work_hours_count_exclude_all(
            datetime.combine(day, datetime.min.time()),
            datetime.combine(day, datetime.max.time().replace(microsecond=0)),
            self.employee,
        )

    def _attendance(self, check_in, check_out):
        return self.env["hr.attendance"].create(
            {"employee_id": self.employee.id, "check_in": check_in, "check_out": check_out}
        )

    @staticmethod
    def _as_client(data):
        # La acción pasa por el cliente en JSON: las fechas vuelven como texto
        return json.loads(json.dumps(data, default=str))

    def _data(self, date_from="2026-11-16", date_to="2026-11-20"):
        return {"ids": self.employee.ids,
                "form": {"from_date": date_from, "to_date": date_to}}

    def test_work_hours(self):
        # Día laborable normal, festivo de OCA y fin de semana
        self.assertAlmostEqual(self._hours(date(2026, 11, 16)), 8.0)
        self.assertAlmostEqual(self._hours(date(2026, 11, 18)), 0.0)
        self.assertAlmostEqual(self._hours(date(2026, 11, 21)), 0.0)

    def test_work_hours_with_leave(self):
        # Una ausencia del empleado por la mañana descuenta sus horas
        self.env["resource.calendar.leaves"].create(
            {"name": "Médico", "calendar_id": self.calendar.id,
             "resource_id": self.employee.resource_id.id,
             "date_from": "2026-11-17 08:00:00", "date_to": "2026-11-17 12:00:00"}
        )
        self.assertAlmostEqual(self._hours(date(2026, 11, 17)), 4.0)

    def test_report_values(self):
        # Lunes: 10 h trabajadas (8 ordinarias y 2 extra); martes: 6 h (todas ordinarias,
        # faltan 2); miércoles festivo: 2 h, todas extra; jueves y viernes sin fichajes:
        # salen con las 8 h que faltan en negativo (igual que en 16.0)
        self._attendance("2026-11-16 08:00:00", "2026-11-16 13:00:00")
        self._attendance("2026-11-16 14:00:00", "2026-11-16 19:00:00")
        self._attendance("2026-11-17 08:00:00", "2026-11-17 14:00:00")
        self._attendance("2026-11-18 10:00:00", "2026-11-18 12:00:00")
        # Sin horas extra aprobadas, el total de extra es la suma de las de cada día
        self.env["hr.attendance.overtime.line"].search(
            [("employee_id", "=", self.employee.id)]
        ).unlink()
        values = self.Report._get_report_values(self.employee.ids, data=self._data())
        days = {d["day"]: d for d in values["attendances"][self.employee.id]}
        self.assertEqual(set(days), {"16", "17", "18", "19", "20"})
        self.assertAlmostEqual(days["16"]["ord_hours"], 8.0)
        self.assertAlmostEqual(days["16"]["extra"], 2.0)
        self.assertEqual(days["16"]["in_out_str"], "08:00-13:00 | 14:00-19:00")
        self.assertAlmostEqual(days["17"]["ord_hours"], 6.0)
        self.assertAlmostEqual(days["17"]["extra"], -2.0)
        self.assertAlmostEqual(days["18"]["ord_hours"], 0.0)
        self.assertAlmostEqual(days["18"]["extra"], 2.0)
        self.assertAlmostEqual(days["19"]["extra"], -8.0)
        self.assertEqual(days["19"]["in_out_str"], "")
        totals = values["totals"][self.employee.id]
        self.assertAlmostEqual(totals["ordinary"], 14.0)
        self.assertAlmostEqual(totals["extra"], -14.0)
        self.assertAlmostEqual(totals["total"], 0.0)

    def test_report_extra_from_approved_overtime(self):
        # Si hay horas extra aprobadas en el periodo, el total de extra sale de ellas
        self._attendance("2026-11-16 08:00:00", "2026-11-16 17:00:00")
        self.env["hr.attendance.overtime.line"].search(
            [("employee_id", "=", self.employee.id)]
        ).unlink()
        self.env["hr.attendance.overtime.line"].create(
            [{"employee_id": self.employee.id, "date": "2026-11-16", "duration": 1.5,
              "status": "approved", "time_start": "2026-11-16 17:00:00",
              "time_stop": "2026-11-16 18:30:00"},
             {"employee_id": self.employee.id, "date": "2026-11-17", "duration": 3.0,
              "status": "refused", "time_start": "2026-11-17 17:00:00",
              "time_stop": "2026-11-17 20:00:00"}]
        )
        values = self.Report._get_report_values(self.employee.ids, data=self._data())
        self.assertAlmostEqual(values["totals"][self.employee.id]["extra"], 1.5)

    def test_wizard_and_render(self):
        self._attendance("2026-11-16 08:00:00", "2026-11-16 16:00:00")
        wizard = self.env["hr.employee.print.attendance.report"].with_context(
            active_ids=self.employee.ids, discard_logo_check=True
        ).create({"from_date": "2026-11-16", "to_date": "2026-11-20"})
        action = wizard.print_report()
        self.assertEqual(action["type"], "ir.actions.report")
        self.assertEqual(action["report_name"], "hr_attendance_report.print_attendance")
        self.assertEqual(action["data"]["ids"], self.employee.ids)
        html = self.env["ir.actions.report"]._render_qweb_html(
            "hr_attendance_report.action_print_attendance", self.employee.ids,
            data=self._as_client(action["data"]),
        )[0].decode()
        self.assertIn("Empleado informe", html)
        self.assertIn("08:00-16:00", html)

    def test_print_as_employee(self):
        # Un empleado sin permisos de RR. HH. imprime su informe desde el empleado público
        self._attendance("2026-11-16 08:00:00", "2026-11-16 16:00:00")
        env = self.env(user=self.user)
        action = env["hr.employee.public"].browse(self.employee.id).print_attendance_report()
        self.assertEqual(action["res_model"], "hr.employee.print.attendance.report")
        wizard = env["hr.employee.print.attendance.report"].with_context(
            active_ids=self.employee.ids
        ).create({"from_date": "2026-11-16", "to_date": "2026-11-20"})
        report_action = wizard.print_report()
        html = env["ir.actions.report"]._render_qweb_html(
            "hr_attendance_report.action_print_attendance", self.employee.ids,
            data=self._as_client(report_action["data"]),
        )[0].decode()
        self.assertIn("08:00-16:00", html)

    def test_print_other_employee_denied(self):
        # Sin ser responsable de asistencias no se imprime el registro de otro empleado
        other = self.env["hr.employee"].create(
            {"name": "Otro empleado", "resource_calendar_id": self.calendar.id}
        )
        env = self.env(user=self.user)
        with self.assertRaises(AccessError):
            env["report.hr_attendance_report.print_attendance"]._get_report_values(
                other.ids, data={"ids": other.ids, "form": {
                    "from_date": "2026-11-16", "to_date": "2026-11-20"}}
            )
