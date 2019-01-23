# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Banking - send debit by email',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'category': 'Banking addons',
    'depends': ['account_payment_order', 'account_payment_return', 'email_template_qweb'],
    'data': ['data/payment_order_data.xml',
             'data/payment_return_data.xml',
             'views/payment_order_view.xml',
             'views/payment_return.xml'],
    'demo': [],
    'description': '''
Send email to partners when payment order is done''',
    'installable': True,
}
