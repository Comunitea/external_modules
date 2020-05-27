# -*- coding: utf-8 -*-
{
    'name': "Ecommerce Autocomplete Search",

    'summary': """
        Odoo ecommerce website product search with dropdown autocomplete""",

    'description': """
        Odoo ecommerce website autocomplete product search with dropdown. 
    """,

    'author': "Beolla Digital",
    'website': "https://beolla.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/templates.xml'
    ],
    # only loaded in demonstration mode
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
    # 'qweb': [
    #     'static/src/xml/exam.xml'
    # ]
    'support': 'support@beolla.com',
    'images': [
        'static/description/banner_screenshot.jpg'
    ]
}