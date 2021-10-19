# © 2021 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Add 347 data in portal',
    'version': '12.0.1.0.0',
    'summary': '',
    'category': 'Website',
    'author': 'Comunitea',
    'maintainer': 'Comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'l10n_es_aeat_mod347',
    ],
    'data': [
        'views/347_portal_templates.xml',
        'security/ir.model.access.csv',
        'security/mod_347_security.xml'
    ],
}
