# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'CMNT Global Discount',
    'version': '8.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'sale',
        'stock_account',
        'report'
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/account_invoice_view.xml",
        "views/report_invoice.xml",
        "views/report_sale_order.xml",
        "views/res_partner_view.xml",
        "views/global_discount_view.xml",
        "security/ir.model.access.csv",

    ],
    "demo": [
    ],
    'test': [
    ],
    "installable": True
}
