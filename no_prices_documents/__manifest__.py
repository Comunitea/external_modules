{
    'name': 'Documents Without Prices',
    'version': '16.0.1.0',
    'description': 'Hide quantities and prices on odoo documents',
    'author': 'Comunitea',
    'website': 'https://comunitea.com/',
    'license': 'LGPL-3',
    'category': 'Custom',
    'depends': [
        'sale',
        'account'
    ],
    'data': [
        'report/sale_report_templates.xml',
        'report/account_report_templates.xml',
        'views/sale_views.xml',
        'views/account_views.xml'
    ],
    'auto_install': False,
    'application': False,
}
