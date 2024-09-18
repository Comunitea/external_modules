{
    'name': 'Pos Restaurant Extension',
    'category': 'Point of Sale',
    'version': "16.0.1.0.0",
    'description': "",
    'author': 'Comunitea servicios Tecnológicos S.L.',
    'website': 'https://www.comunitea.com',
    'depends': [
        'l10n_es_pos',
        'pos_restaurant',
        'pos_report_session_summary',
        #'pos_order_return', OBSOLETO
        'pos_hr'
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_restaurant_extended/static/src/js/*.js',
            'pos_restaurant_extended/static/src/js/*/*/*.js',
            'pos_restaurant_extended/static/src/js/*/*/*/*.js',
            'pos_restaurant_extended/static/src/xml/*.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
