# © 2019 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Sale Section Variant MGMT',
    'summary': 'Manage promotions in PoS',
    'version': '11.0.0.0.1',
    'category': 'Sale',
    'author': 'Comunitea ',
    'website': 'https://github.com/OCA/pos',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'product',
        'sale_order_variant_mgmt'
    ],
    'data': [
        'wizard/sale_manage_variant_view.xml'
    ],
    'installable': True,
}
