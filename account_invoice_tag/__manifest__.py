# -*- coding: utf-8 -*-
# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account invoice tags',
    'version': '10.0.1.0.0',
    'depends': [
        'account',
    ],
    'author': "Comunitea",
    'license': "AGPL-3",
    'summary': '''Allow to set tags to categorize invoices''',
    'website': 'http://www.comunitea.com',
    'data': ['views/account_invoice_view.xml',
             'views/account_invoice_tag_view.xml',
             'security/ir.model.access.csv'],
    'installable': True,
    'auto_install': False,
}
