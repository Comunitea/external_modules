# -*- coding: utf-8 -*-
# Copyright 2015 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Advance Payment",
    "version": "10.0.1.0.0",
    "author": "Comunitea",
    'website': 'www.comunitea.com',
    "category": "Purchases",
    "description": """Allow to add advance payments on purchases and then use
 its on invoices""",
    "depends": ["purchase", "account"],
    "data": ['wizard/purchase_advance_payment_wzd_view.xml',
             'views/purchase_view.xml',
             'security/ir.model.access.csv'],
    "installable": True,
}
