# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Payment Manual Exchange Rate",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Set the exchange rate manually on payments in foreign currency",
    "author": "Comunitea",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": [
        "views/account_payment_views.xml",
        "wizard/account_payment_register_views.xml",
    ],
    "installable": True,
}
