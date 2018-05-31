# -*- coding: utf-8 -*-
# Copyright 2015-2017 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Payments Due list check received",
    'version': '10.0.1.0.0',
    'category': 'Generic Modules/Payment',
    'author': 'Comunitea',
    'website': 'http://comunitea.com',
    'license': 'AGPL-3',
    "depends": [
        'account_due_list',
        'account_accountant',
    ],
    "data": [
        'views/payment_view.xml',
    ],
    "installable": True,
}
