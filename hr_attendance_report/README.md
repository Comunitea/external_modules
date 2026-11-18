# Attendance report

Informe PDF de registro de jornada por empleado (artículos 34.7 y 34.9 del Estatuto de los
Trabajadores).

## Uso

- Desde la lista o el formulario de empleados: acción **Print attendance report**, con las fechas
  desde y hasta.
- Desde el empleado público: botón **Print Attendance Report** en la cabecera. Cualquier empleado
  puede imprimir su propio registro; el de otros, solo quien tiene el grupo de responsable de
  asistencias (`hr_attendance.group_hr_attendance_officer` o superior).

Por cada día con fichajes o con horas previstas: entradas y salidas, horas ordinarias y horas
extra (negativas si faltan horas). Al final, los totales: total, ordinarias, complementarias,
extra y media diaria. El CCC de la compañía (campo `ccc`, en el formulario de la compañía) sale en
la cabecera.

## Cálculo de las horas

- Horas previstas del día: las del horario del empleado, menos los festivos de OCA
  (`hr_holidays_public`, por país y provincia de la dirección de trabajo) y menos sus ausencias.
- Horas ordinarias: las trabajadas, como máximo las previstas. El resto son extra.
- Total de extra del periodo: si hay horas extra aprobadas (`hr.attendance.overtime.line` con
  estado aprobado) se usa su duración; si no, la suma de las extra de cada día.

## Notas de la migración a 19.0

- `resource.calendar.attendance` ya no tiene fechas de validez (`date_from`/`date_to`): se quita
  el tratamiento de "días especiales" de 16.0. Los horarios con varios periodos por fechas (p. ej.
  jornada de verano) se tienen que rehacer en 19.0 (un horario por periodo, en la versión del
  empleado).
- Las horas extra pasan de `hr.attendance.overtime` a `hr.attendance.overtime.line`.
- El campo `ssnid` ya sale en el formulario del empleado de 19.0: se quita la vista que lo añadía.
