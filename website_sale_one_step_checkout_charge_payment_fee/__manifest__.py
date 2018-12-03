# -*- coding: utf-8 -*-
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'External: Charge payment fee in one step checkout',
    'version': '1.0',
    'summary': 'Allows to use payment fee in OSC.',
    'author': '© 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>',
    'license': 'AGPL-3',
    'category': 'eCommerce',
    'depends': [
        'payment_acquirer_by_amount',
        'website_sale_one_step_checkout',
        'website_sale_charge_payment_fee'
    ],
    'data': [
        'views/templates.xml'
    ],
    'images': [
    ],
    'website': 'http://www.comunitea.com',
    'installable': True,
}
