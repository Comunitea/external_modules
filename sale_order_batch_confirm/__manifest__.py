# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Sale Order Batch confirm',
    'version': '0.0.1',
    'author': 'Comunitea ',
    "category": "Sales",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'queue_job'
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        'views/sale_config_settings_view.xml',
    ],
    "installable": True,
    'application': False,
}
