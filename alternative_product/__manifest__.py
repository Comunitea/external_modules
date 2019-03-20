# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Alternative product in sale orders',
    'summary': 'Add kanban view in sale orders',
    'version': '11.0.1.0.0',
    'category': 'partner',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'website_sale',  # Mete el campo de productos alternativos
    ],
    'data': [
        'views/sale_order.xml',
        'wizard/product_product.xml'
    ],
}