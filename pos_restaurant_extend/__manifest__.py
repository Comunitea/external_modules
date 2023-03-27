# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Pos Restaurant Extension',
    'category': 'Point of Sale',
    'version': "14.0.1.0.0",
    'description': "",
    'author': 'Comunitea servicios Tecnológicos S.L.',
    'website': 'https://www.comunitea.com',
    'depends': [
        'l10n_es_pos',
        'pos_restaurant',
        'pos_report_session_summary',
        'pos_order_return',
        'pos_hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/pos_ext.xml',
        'views/pos_category.xml',
        'views/pos_config.xml',
        'views/restaurant_floor.xml',
        'views/restaurant_printer.xml',
        'views/report_saledetails.xml',
        'views/pos_session_view.xml',
        'views/pos.xml',
        'reports/pos_report.xml',
    ],
    'installable': True,
    'application': False,
    'qweb': [
        'static/src/xml/pos.xml',
        'static/src/xml/ServiceSelectionButton.xml',
        'static/src/xml/TableWidget.xml',
        'static/src/xml/Chrome.xml',
        'static/src/xml/ChromeWidgets/ReloadOrdersButton.xml',
        'static/src/xml/ProductsWidgetControlPanel.xml',
        'static/src/xml/HomeCategoryBreadcrumb.xml',
    ],
    'auto_install': False,
}
