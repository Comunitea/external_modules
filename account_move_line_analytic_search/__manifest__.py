{
    'name': 'Analytic Distribution Search in account',
    'summary': 'Analytic Distribution Search in account move lins',
    'version': "16.0.1.0.0",
    'category': 'Accounting',
    'website': 'https://comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'account_financial_report',
    ],
    'data': [
        'views/account_move_line_view.xml',
    ],
}