# -*- coding: utf-8 -*-
# © 2009 Albert Cervera i Areny <http://www.nan-tic.com)>
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# © 2011 Pexego Sistemas Informáticos.
#        Alberto Luengo Cabanillas <alberto@pexego.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Nan Partner Risk',
    'version': '10.0.0.0.0',
    'category': 'Custom',
    'license': 'AGPL-3',
    'author': "Comunitea, ",
    'depends': [
        'base',
        'sale',
        'account',
    ],
    'data': [
        'security/nan_partner_risk_groups.xml',
        'wizard/open_risk_window_view.xml',
        'views/res_partner_view.xml',
        'views/sale_view.xml',
        'views/account_view.xml',
    ],
    'installable': True,
}
