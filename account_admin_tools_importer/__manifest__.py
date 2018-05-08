# -*- coding: utf-8 -*-
# © 2015 Pexego Sistemas Informáticos
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Admin Importation Tools",
    "version": "11.0.1.0",
    "author": "Pexego, Comunitea",
    "website": "http://www.comunitea.com",
    "category": "Enterprise Specific Modules",
    "description": """Account Importation Tools for Administrators

Import tools:

- Import accounts from CSV files. This may be useful to import the initial
  accounts into Odoo.

- Import account moves from CSV files. This may be useful to import the initial
  balance into Odoo.
            """,
    "depends": ['base',
                'account'],
    "data": ['wizard/account_importer.xml',
             'wizard/account_move_importer.xml'],
    "installable": True,
    'license': 'AGPL-3'
}
