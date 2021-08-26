# © 2017 Comunitea Servicios Tecnológicos S.L.
#        (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Manual Payment Term from Invoice",
    'version': '14.0.1.0.0',
    'category': 'Generic Modules/Payment',
    'author': 'Odoo Community Association (OCA), '
              'Comunitea, ',
    'website': 'https://www.comunitea.com',
    'license': 'AGPL-3',
    "depends": [
        'account',
    ],
    "data": [
        'views/account_move_view.xml',
    ],
    "installable": True
}
