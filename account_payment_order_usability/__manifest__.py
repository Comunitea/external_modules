# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Usability enhancements Payment Orders',
    'version': '10.0.0.1.0',
    'author': "Comunitea",
    'depends': ['account_payment_order', 'account_due_list'],
    'category': 'Extra Tools',
    'description': """
- Check if invoice has mandate before include it to payment order
- Filter that show if invoice is already in payment order
    """,
    'website': 'https://comunitea.com',
    'data': ['views/account_invoice_view.xml'],
    'installable': True,
}
