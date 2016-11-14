# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Comunitea custom snippets',
    'summary': '',
    'version': '8.0.1.0.0',
    'category': 'Theme',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'website',
        'website_crm',
        'web',
    ],
    'data': [
        'views/assets.xml',
        'views/snippet.xml'
    ],
}
