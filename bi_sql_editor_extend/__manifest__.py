# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'BI SQL Editor',
    'summary': 'Extension for BI SQL Editor. Not need to recreate model for editing views and fields',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Reporting',
    'author': 'Comunitea',
    'website': 'https://github.com/OCA/reporting-engine',
    'depends': [
        'base',
        'bi_sql_editor',
    ],
    'data': [
        'views/view_bi_sql_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
}
