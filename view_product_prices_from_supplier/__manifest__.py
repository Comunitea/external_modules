# -*- coding: utf-8 -*-
# Copyright 2019 Javier Colmenero Fernández <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'View Product Prices From Supplier',
    'author': 'Comunitea',
    'category': 'Custom',
    'license': 'AGPL-3',
    'website': 'http://www.comunitea.com',

    'depends': [
        'product',
        'purchase',
    ],
    'data': [
        'views/res_partner_view.xml'
    ],
    'installable': True,
}
