# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Advance Payment Manual Exchange Rate",
    "version": "19.0.1.0.0",
    "category": "Purchase Management",
    "summary": "Set the exchange rate manually on purchase advance payments",
    "author": "Comunitea",
    "license": "AGPL-3",
    "depends": ["purchase_advance_payment", "account_payment_manual_rate"],
    "data": ["wizard/purchase_advance_payment_wizard_view.xml"],
    "auto_install": True,
    "installable": True,
}
