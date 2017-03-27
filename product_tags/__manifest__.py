# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julius Network Solutions SARL <contact@julius.fr>
# Copyright (C) 2015 credativ ltd. <info@credativ.co.uk>
# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Tags",
    "version": '10.0.1.0.0',
    "author": "Julius Network Solutions",
    "website": "http://julius.fr",
    "category": "Sales Management",
    "depends": [
        'product',
        'sale',
    ],
    "description": """
    Add tags in products like it's done for the partners
    """,
    "demo": [],
    "data": [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
