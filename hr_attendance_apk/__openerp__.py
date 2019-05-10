# -*- coding: utf-8 -*-
# Copyright 2017 Comunitea Servicios Tecnológicos S.L.

{
    'name': 'HR Attendance APK',
    'version': '8.0.1.0.0',
    'category': 'Human Resources',
    'author': 'Comunitea,',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'security/ir_group.xml',
        'security/ir.model.access.csv',
        'views/hr_attendance_view.xml',
        'views/clock_company_apk.xml',
    ],
}
