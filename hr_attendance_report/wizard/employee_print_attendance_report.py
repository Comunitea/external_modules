# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
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

from openerp import models, fields, api, exceptions, _


class EmployeePrintAttendanceReport(models.TransientModel):

    _name = 'hr.employee.print.attendance.report'

    from_date = fields.Date('From', required=True)
    to_date = fields.Date('To', required=True)

    @api.multi
    def print_report(self):
        self.ensure_one()
        datas = {'ids': self._context.get('active_ids', [])}
        res = {'from_date': self.from_date, 'to_date': self.to_date}
        datas['form'] = res
        return self.env['report'].get_action(
            self, 'hr_attendance_report.print_attendance', data=datas)
