# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Base Warehouse App',
    'summary': 'Add code and configs for warehouse apk',
    'version': '11.0.1.0.0',
    'category': 'Warehouse',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_picking.xml'
    ],
}
