# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos S.L. (<http://comunitea.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Direct Debit with refunds',
    'version': '8.0.0.0.0',
    'license': 'AGPL-3',
    'author': 'Comunitea',
    'website': 'https://github.com/OCA/bank-payment',
    'category': 'Banking addons',
    'depends': ['account_direct_debit',
                'account_banking_mandate'],
    'data': ['views/account_payment.xml',
             'views/account_invoice.xml'],
    'installable': True,
}
