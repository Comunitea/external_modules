# © 2018 Comunitea - Santi Argüeso <santi@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Cash Forecast',
    'version': '12.0.1.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    "description": """Cash forecast for configured periods""",
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_payment_order',
        'l10n_es_account_banking_sepa_fsdd',
        'account_due_list'
    ],
    'contributors': [
        "Comunitea ",
        "Santi Argüeso <santi@comunitea.com>",
    ],
    "data": [
        'views/cash_forecast_view.xml',
        'security/ir.model.access.csv',
        'security/cash_forecast_security.xml'
    ],
    "installable": True
}
