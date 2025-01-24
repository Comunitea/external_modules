# -*- coding: utf-8 -*-
# © 2024 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Attendance report portal',
    'version': '16.0.1.0.0',
    'summary': '',
    'category': 'Human Resources',
    'author': 'comunitea',
    'maintainer': 'comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'hr_attendance_report',
        'hr_attendance',
        'portal'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_attendance_report_views.xml',
        'views/hr_employee_view.xml',
        'views/res_config_settings_view.xml',
        'templates/employee_attendance_report_templates.xml',
        'reports/hr_employee_attendance_report.xml',
        'data/cron.xml',
    ],
    'installable': True,
}
