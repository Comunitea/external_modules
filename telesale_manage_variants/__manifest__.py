# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Telesale Manage Variants',
    'version': '10.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'telesale',
        'custom_sale_order_variant_mgmt'
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        'views/telesale_assets.xml'
    ],
    'qweb': [
        'static/src/xml/new_order_template.xml',
        'static/src/xml/popups_template.xml',
    ],
    "installable": True
}
