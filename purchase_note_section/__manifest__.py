# -*- coding: utf-8 -*-
{
    'name': "purchase_note_section",

    'summary': """
      Odoo 12's Purchase Order Note and Section
      """,

    'description': """
    This addon allows to add note and section in Odoo 12 Purchase Order form.
    """,

    'author': "TL Dev Tech",
    'website': "https://www.tldevtech.com",
    'license': 'LGPL-3',
    'category': 'Purchases',
    'version': '12.1.0.0',
    'images': ['static/description/images/main_screenshot.png'],
    'depends': ['purchase'],
    'data': [
        'views/views.xml',
        'views/report_purchase.xml',
    ],

}
