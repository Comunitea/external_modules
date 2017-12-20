# -*- coding: utf-8 -*-
# © 2017 Comunitea Servicios Tecnológicos S.L. (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Purchase Variant Management",
    'version': '10.0.1.0.0',
    'category': 'Textile Vertical',
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'license': 'AGPL-3',
    "depends": [
        'purchase',
        'web_widget_x2many_2d_matrix',
    ],
    "data": [
        'wizard/purchase_manage_variant_view.xml',
        'views/purchase_view.xml',
        'views/widget_assets.xml',
    ],
    "installable": True
}
