
{
    "name": "Account Review Break Payments",
    "version": "13.0.0.0.0",
    "author": "Comunitea",
    "website": "https://www.comunitea.com",
    "category": "Custom Module",
    "description": """
        Review Payments canceled but in open state. Add as new user permition
        called Review payments wizard to use the funcionality in Menu
        Account/Account
    """,
    "depends": ['account'],
    "data": [
        'security/groups_data.xml',
        'security/ir.model.access.csv',
        'views/account_payment.xml',
        'wizard/review_payments_wzd.xml',
    ],
    "installable": True,
    'license': 'AGPL-3'
}
