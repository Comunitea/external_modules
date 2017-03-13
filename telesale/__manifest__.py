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
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        'views/ts_config_view.xml',
        'views/telesale_menus.xml',
        'views/telesale.xml',
        'views/ts_templates.xml',
    ],
    "installable": True,
    'application': True,
    'qweb': ['static/src/xml/new_order_template.xml'],
}
