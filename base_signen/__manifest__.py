# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Base signen',
    'version': '10.0.1.0.0',
    'summary': 'Base module for signen integration',
    'category': '',
    'author': 'Comunitea',
    'maintainer': 'Comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'queue_job'
    ],

    'external_dependencies': {
        'python': [
            'requests',
            'Crypto'
        ],
    },
    'data': [
        'views/signen_configuration.xml',
        'views/res_company.xml',
        'wizard/signen_create_user.xml',
        'data/ir_config_parameter.xml',
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'security/signen_security.xml'
    ],
    'installable': True,
}
