# © 2023 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Payment Return Invoice Resend",
    "version": "12.0.1.0.0",
    "category": "Accounting",
    "author": "Comunitea",
    "website": "www.comunitea.com",
    "license": "AGPL-3",
    "depends": [
        "account_payment_return",
    ],
    "data": [
        'data/mail_template.xml',
        'views/account_invoice.xml',
        'views/res_company_view.xml',
        'views/account_journal_view.xml',
    ],
    "installable": True,
}
