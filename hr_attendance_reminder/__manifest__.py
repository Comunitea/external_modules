# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Attendance reminder',
    'version': '16.0.1.0.0',
    'summary': '',
    'category': 'Human Resources',
    'author': 'comunitea',
    'maintainer': 'comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'hr_attendance',
        'hr_holidays_public',
    ],
    'data': [
        'data/ir_cron.xml',
        'data/mail_template.xml',
        'views/resource_calendar.xml',
    ],
    'installable': True,
}
