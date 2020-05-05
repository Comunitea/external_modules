# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'delivery carrier label comunitea fixes',
    'version': '12.0.1.0.0',
    'summary': 'Custom fixes for base_delivery_carrier_label',
    'category': 'Delivery',
    'author': 'Comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'base_delivery_carrier_label',
        'base_report_to_printer'
    ],
    'data': [
        'views/delivery_carrier.xml',
        'views/stock_picking.xml',
        'views/carrier_account.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml'
    ],
}
