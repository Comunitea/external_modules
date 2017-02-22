# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos (<http://www.comunitea.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Percentage of margins in Sales Orders',
    'version': '1.0',
    'category': 'Sales Management',
    'description': """
    """,
    'author': 'Comunitea',
    'depends': ['sale'],
    'data': ["views/sale_view.xml",
             "views/sale_report_view.xml"],
    'contributors': [
        "Jesús Ventosinos Mayor <jesus@pexego.es>",
        "Omar Castiñeira Saavedra <omar@comunitea.com>",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    'auto_install': False,
    'installable': False,
}
