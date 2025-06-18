# Copyright 2024 Comunitea - Javier Colmenero
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, time

from dateutil import rrule
from pytz import timezone, utc

from odoo import models

from odoo.addons.resource.models.utils import Intervals


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"
        
    def get_work_hours_count_exclude_all(
            self, start_dt, end_dt, employee, 
            compute_leaves=True, domain=None):
        """
        Versión de get_work_hours_count que debería excluir tanto las
        ausencias de Odoo como los festivos de OCA.
        Añado el empleado
        En la original tiene un if con el compute_leaves, de tal modo que si
        es True intenta excluir las hr.leaves de Odoo con _work_intervals_batch
        (sin exito para una ausencia de empleado)
        En caso de ser False se llama otra función _attendance_intervals_batch.
        El módulo de hr_holidays_public añade la funcionalidad de excluir los
        hr.holidays.public pero no se puede hacer junto con las ausencias de 
        Odoo.
        Aquí primero llamo con el contexto para excluir los festicvos de OCA,
        si el resultado es 0 lo devuelvo, sino corrijo la llamada a 
        _work_intervals_batch, para que descuente las horas de las ausencias, 
        que parece faltarle especificar el recurso del empleado, ya que sino no
        descuenta las horas o días de ausencias (Vacaciones, asuntos propio...)
        """
        self.ensure_one()
        # Necesario para excluir los festivos de OCA, y el employee_id para
        # que lo haga por provincias también
        self = self.with_context(
            exclude_public_holidays=True, employee_id=employee.id)
        # Set timezone in UTC if no timezone is explicitly given
        if not start_dt.tzinfo:
            start_dt = start_dt.replace(tzinfo=utc)
        if not end_dt.tzinfo:
            end_dt = end_dt.replace(tzinfo=utc)
        
        # Primero consulto los festivos generales
        intervals = employee.resource_calendar_id.\
            _attendance_intervals_batch(
                start_dt, end_dt, employee.resource_id)[employee.resource_id.id]
        hours_without_holidays = sum(
            (stop - start).total_seconds() / 3600
            for start, stop, meta in intervals
        )
        # Era festivo, devuelvo 0
        if not hours_without_holidays:
            return hours_without_holidays
        
        # Para que odoo descuernte las ausencias necesito pasarle el recurso del empleado
        intervals = self._work_intervals_batch(
            start_dt, end_dt, domain=domain, resources=employee.resource_id)[employee.resource_id.id]

        return sum(
            (stop - start).total_seconds() / 3600
            for start, stop, meta in intervals
        )
