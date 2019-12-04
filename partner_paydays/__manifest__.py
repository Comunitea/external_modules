# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Paydays",
    "version": "12.0.0.0.0",
    "description": """"This module adds fields to introduce partner's paydays
& holidays. It also allows due date in customer invoices to take into account
vacations if the partner doesn't pay during that period.""",
    "author": "Nan,Pexego \n contributor readylan, Comunitea",
    "website": "http://www.NaN-tic.com, http://www.comunitea.com",
    "depends": ["account"],
    "category": "Custom Modules",
    "data": [
        "views/partner_paydays_view.xml",
        "views/account_invoice.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
