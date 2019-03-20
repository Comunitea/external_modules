# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Default partner by type',
    'summary': 'Add default_partner by type in childs',
    'version': '11.0.1.0.0',
    'category': 'partner',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base'

    ],
    'data': [
        'views/res_partner_view.xml',
    ],
}