# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Active Banking mandates",
    "description": """
       Allows to deactive banking mandates
    """,
    "version": "11.0.1.0.0",
    "author": "Comunitea",
    'license': 'AGPL-3',
    "website": "http://www.comunitea.com",
    "depends": ["account_banking_mandate", "res_partner_bank_active"],
    "category": "Accounting",
    "data": ['views/account_banking_mandate_view.xml'],
    'installable': True,
}
