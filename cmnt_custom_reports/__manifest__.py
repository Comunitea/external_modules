# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'CMNT Custom Reports',
    'version': '8.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'account_payment_partner',
        'report'
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        "views/report_invoice.xml",
        "views/report_sale_order.xml",
        "views/layouts.xml",
    ],
    "demo": [
    ],
    'test': [
    ],
    "installable": False
}
