# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website sale filter countries',
    'summary': '',
    'version': '8.0.1.0.0',
    'category': 'Uncategorized',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': False,
    'depends': [
        'website_sale',
        'website_snippet_country_dropdown'
    ],
    'data': [
        'views/res_country.xml',
        'views/snippet.xml'
    ],
}
