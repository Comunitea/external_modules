{
    "name": "Web Widget Sale Product Label Section Editable",
    "version": "18.0.0.1.0",
    "description": "This module allows to edit the sale product label section",
    "author": "Comunitea",
    "website": "www.comunitea.com",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": [
        "account",
        "sale",
    ],
    "auto_install": False,
    "application": False,
    "assets": {
        'web.assets_backend': [
            'web_widget_product_label_section/static/src/xml/sale_product_field.xml',
        ],
    }
}