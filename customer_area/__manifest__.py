# -*- coding: utf-8 -*-
# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Customer area',
    'version': '10.0.1.0.0',
    'depends': [
        'sales_team',
    ],
    'author': "Comunitea",
    'license': "AGPL-3",
    'summary': '''New dimension of customer's categorization''',
    'website': 'http://www.comunitea.com',
    'data': ['views/res_partner_area_view.xml',
	     'views/res_partner_view.xml',
	     'security/ir.model.access.csv'],
    'installable': False,
    'auto_install': False,
}
