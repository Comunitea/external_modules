{
    'name': 'Pos Restaurant Extension',
    'category': 'Point of Sale',
    'version': "17.0.1.0.0",
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
        'views/pos_category.xml',
        'views/res_config_settings_views.xml',
        'views/pos_session_views.xml',
        'views/pos.xml',
        'views/report_saledetails.xml',
        'views/restaurant_floor.xml',
        'views/restaurant_printer.xml',
        'reports/pos_report.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_restaurant_extend/static/src/js/*.js',
            'pos_restaurant_extend/static/src/js/*/*.js',
            'pos_restaurant_extend/static/src/js/*/*/*.js',
            'pos_restaurant_extend/static/src/js/*/*/*/*.js',
            'pos_restaurant_extend/static/src/xml/*.xml',
            'pos_restaurant_extend/static/src/xml/*/*.xml',
            'pos_restaurant_extend/static/src/css/*.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
