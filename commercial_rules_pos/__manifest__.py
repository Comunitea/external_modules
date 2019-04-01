# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Commercial Rules PoS',
    'summary': 'Manage promotions in PoS',
    'version': '11.0.0.0.1',
    'category': 'Point of Sale',
    'author': 'Comunitea ',
    'website': 'https://github.com/OCA/pos',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'commercial_rules'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'application': False,
    'installable': True,
}
