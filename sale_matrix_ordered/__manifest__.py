# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Matrix Ordered',
    'version': '10.0.1.0.0',
    'author': 'Comunitea',
    'category': 'Custom',
    'license': 'AGPL-3',
    'website': 'http://www.comunitea.com',

    'depends': [
        'sale_order_variant_mgmt',
        'widget_matrix_ordered',
    ],
    'demo': [],
    'data': [
        'wizard/sale_manage_variant_view.xml',
    ],
    'installable': True,
}
