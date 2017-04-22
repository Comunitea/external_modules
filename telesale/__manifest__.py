# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Telesale',
    'version': '0.0.1',
    'author': 'Comunitea ',
    "category": "Sales",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'web',
        'product',
        'commercial_rules',
        'stock'  # stock_available ProductInfoWifget, move to other module?
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/ts_config_view.xml',
        'views/telesale_menus.xml',
        'views/telesale_assets.xml',
        'views/ts_templates.xml',
        'views/sale_view.xml',
    ],
    "installable": True,
    'application': True,
    'qweb': [
        'static/src/xml/key_shorts_template.xml',
        'static/src/xml/new_order_template.xml',
        'static/src/xml/order_history_template.xml',
        'static/src/xml/product_catalog_template.xml',
        'static/src/xml/customer_list_template.xml',
        'static/src/xml/popups_template.xml',
    ],
}
