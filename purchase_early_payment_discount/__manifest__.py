# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Early payment discount',
    'summary': """ Adds early payment discount to purchases
                    """,
    'version': '10.0.1.0.0',
    'author': 'Comunitea',
    'maintainer': 'Comunitea',
    'license': 'AGPL-3',
    'depends': ['base', 
                'purchase',
                'sale_early_payment_discount'
    ],
    'category': 'Custom Specific Modules',
    'data': [
        'views/purchase_view.xml',
        'views/account_invoice_view.xml',
        'report/purchase_order.xml'
    ],
    'installable': True
}
