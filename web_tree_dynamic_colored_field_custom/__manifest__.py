# Copyright 2015-2018 Camptocamp SA, Damien Crier
# Copyright 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Colorize field in tree views. Custom',
    'summary': 'Allows you to dynamically color fields on tree views',
    'category': 'Hidden/Dependency',
    'version': '12.0.1.0.0',
    'depends': ['web', 'web_tree_dynamic_colored_field'],
    'author': "Camptocamp, Therp BV, Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/web',
    'demo': [
        "demo/res_users.xml",
    ],
    'data': [
        'views/web_tree_dynamic_colored_field.xml',
    ],
    'installable': True,
}
