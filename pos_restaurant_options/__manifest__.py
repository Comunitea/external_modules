{
    'name': 'Product Restaurant Options',
    'version': "17.0.1.0.0",
    'description': 'Product Restaurant Options',
    'depends': [
        'mrp',
        'pos_product_template_configurator',
        'pos_restaurant_extend'
    ],
    'author': 'Comunitea servicios Tecnológicos S.L.',
    'website': 'https://www.comunitea.com',
    'data': [
        'views/mrp_view.xml',
        'views/product.xml',
        # 'views/assets.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_restaurant_options/static/src/js/*.js',
            'pos_restaurant_options/static/src/js/*/*/*.js',
            'pos_restaurant_options/static/src/xml/*/*.xml',
        ],
    },
    'installable': True,
}
