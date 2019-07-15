# -*- coding: utf-8 -*-

{
    'name': 'Biometric Device Integration',
    'version': '1.3.0',
    'author': 'OpenPyme',
    'category': 'Human Resources',
    'website': 'http://www.openpyme.mx',
    'license': 'GPL-3',
    'depends': ['hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/biometric_data_view.xml',
        'views/biometric_machine_view.xml',
        'views/hr_attendance.xml',
        'views/biometric_user_view.xml',
        'wizard/biometric_user.xml',
        'wizard/biometric_data.xml',
        'cron_task/biometric_data.xml',
    ],
    'installable': True,
    'external_dependencies': {
        'python': [
            'zk',
        ],
    },
}
