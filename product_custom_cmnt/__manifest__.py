# -*- coding: utf-8 -*-
# © 2018 Comunitea Servicios Tecnológicos S.L. (http://comunitea.com)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

{
    'name': "Product Castegorización Info CMNT",
    'summary': "Add custom fields in products",
    'category': 'Product',
    'version': '10.0.1.0.0',
    'depends': [
        'product',
    ],
    'data': [
            'security/ir.model.access.csv',
            'views/custom_info_views.xml',
            'wizard/product_template_custom_values_wzd.xml',
            'views/product_template_view.xml'

    ],
    'author': "Comunitea Servicios Tecnológicos",
    'website': "http://www.comunitea.com",
    'license': 'LGPL-3',
    'installable': True,
}