# -*- coding: utf-8 -*-
# © 2017 Comunitea Servicios Tecnológicos S.L. (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Purchase Matrix Ordered",
    'version': '10.0.1.0.0',
    'category': 'Custom',
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'license': 'AGPL-3',
    "depends": [
        'purchase_order_variant_mgmt',
        'widget_matrix_ordered',
    ],
    "data": [
        'wizard/purchase_manage_variant_view.xml',
    ],
    "installable": True
}
