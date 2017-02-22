# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Customer Expense Account',
    'version': '8.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'account_analytic_default'
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        "wizard/customer_expense_wzd_view.xml",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
        "views/expense_structure_view.xml",
        "views/expense_type_view.xml",
        "views/expense_account_menu.xml",
        "views/customer_expense_report.xml",
        "views/report.xml",
        "security/ir.model.access.csv",
        "security/expense_structure_security.xml",
    ],
    "demo": [
        "demo/data_demo.xml",
    ],
    "installable": False
}
