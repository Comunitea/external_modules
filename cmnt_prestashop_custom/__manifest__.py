# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Prestashop customizations from Comunitea',
    'version': '12.0.1.0.0',
    'category': 'Connector',
    'author': 'Comunitea',
    'maintainer': 'Comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'connector_prestashop',
        'base_location'
    ],
    'data': [
        'views/prestashop_backend.xml',
        'views/sale_order.xml',
        'views/sale_order_state.xml'
    ],
}
