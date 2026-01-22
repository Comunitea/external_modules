{
    'name': 'Web Required Field Style',
    'version': '18.0.1.0.0',
    'description': 'Restore purple background for required fields',
    'author': 'Comunitea',
    'website': 'www.comunitea.com',
    "contributors": ["Comunitea","Miguel Vázquez <miguel@comunitea.com>"],
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': [
        'web',
    ],
    'auto_install': False,
    'application': False,
    "assets": {
        "web.assets_backend": [
            "/web_required_field_style/static/src/**/*.scss",
        ],
    },
}