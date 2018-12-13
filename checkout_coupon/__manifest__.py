# -*- coding: utf-8 -*-
# © 2018 Comunitea
# Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'OSC: Discount Coupons',
    'version': '1.0',
    'summary': 'Discount Coupons for OneStepCheckout',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'category': 'Website',
    'depends': [
        'website_sale_one_step_checkout_delivery',
        'website_sale_one_step_checkout_charge_payment_fee'
    ],
    'data': [
        'views/coupons.xml',
        'views/history.xml',
        'views/sale_order.xml',
        'views/settings.xml',
        'views/menu.xml',
        'views/links.xml',
        'templates/checkout.xml'
    ],
    'images': [
        'static/description/icon.png',
    ],
    'website': 'http://www.comunitea.com',
    'installable': True,
}
