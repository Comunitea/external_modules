# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Order line canceled qty',
    'summary': 'Canceled qty in moves to order lines (sale and purchase)',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'stock',
        'purchase',
        'purchase_stock',
        'sale'
    ]
}
