# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Virtual stock conservative on products",
    'version': '12.0.1.0.0',
    'category': 'Products',
    'description': """Add virtual stock conservative computation to products. stock real - outgoing stock""",
    'author': 'Comunitea',
    'website': 'www.comunitea.com',
    "depends": ['stock', 'stock_available_unreserved'],
    "data": ["views/product_view.xml"],
}
