# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'RMA warranty',
    'version': "17.0.1.0.0",
    'summary': 'Warranty management on products and RMA',
    'category': '',
    'author': 'Comunitea',
    'maintainer': 'Comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'contributors': [
    ],
    'depends': [
        'rma',
        'product_warranty',
    ],
    'data': [
        'views/stock_lot.xml',
        'data/ir_config_parameter.xml',
        'views/rma.xml'
    ],
}
