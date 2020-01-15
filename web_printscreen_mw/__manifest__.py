{
    'name': 'Web Printscreen MW',
    'version': '12.0.1.0',
    'category': 'Web',
    'description': """
        Module to export current active tree view in to excel report
    """,
    'author': 'Manexware S.A.',
    'website': 'http://www.manexware.com',
    'depends': ['web'],
    'external_dependencies': {'python': ['trml2pdf']},
    'data': ['views/web_printscreen_mw.xml'],
    'qweb': ['static/src/xml/web_printscreen_export.xml'],
    'installable': True,
    'auto_install': False,
    'web_preload': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
