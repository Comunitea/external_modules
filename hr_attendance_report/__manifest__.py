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


{
    'name': 'Attendance report',
    'summary': '',
    'version': "15.0.0.0.0",
    'category': 'Human Resources',
    'website': 'https://comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/paperformat.xml',
        'wizard/employee_print_attendance_report.xml',
        'reports/hr_employee_attendance_report.xml',
        'reports/hr_attendance_report.xml',
        'views/company_views.xml',
        'views/hr_employee_views.xml'
    ],
}
