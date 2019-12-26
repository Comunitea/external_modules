# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Procurements by CAtegory',
    'summary': 'Run only orderpoints for selected categories',
    'version': '12.0.1.0.0',
    'category': 'partner',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'stock',
    ],
    'data': [
        'wizard/procure_category.xml'
    ],
}
