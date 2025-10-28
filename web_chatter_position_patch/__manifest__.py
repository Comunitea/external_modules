{
    'name': 'Web chatter position patch',
    'version': '18.0.1.0.0',
    'description': 'Custom module to improve the side position of the chatter in form views.',
    'author': 'Comunitea',
    'website': 'www.comunitea.com',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': [
        'web_chatter_position',
    ],
    'auto_install': False,
    'application': False,
    "assets": {
        "web.assets_backend": [
            "/web_chatter_position_patch/static/src/**/*.js",
            "/web_chatter_position_patch/static/src/**/*.scss",
        ],
    },
}