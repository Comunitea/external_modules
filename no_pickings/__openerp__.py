# -*- coding: utf-8 -*-
{
    'name': 'No-pickings',
    'version': '0.1',
    'category': 'Tools',
    'description': """
        This module allows not pick the moves generated from sale orders,
 setting 'no picking' field. It adds wizard that allows to create a picking
 from moves of different sale orders, allways that order have the same
 shipping partner.
    """,
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'depends': ['base','sale_stock'],
    'data': [
        'no_pickings_view.xml',
        'wizard/moves_to_pick_view.xml'
    ],
    'installable': True,
}
