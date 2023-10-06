# © 2023 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Virtual Tracking",
    "version": "16.0.0.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "author": "Comunitea, ",
    "depends": [
        "mrp",
        "stock",
        "web_widget_color",
    ],
    "data": [
        "security/ir.model.access.csv",
        # "views/stock_move.xml",
        # "views/stock_picking.xml",
        "views/stock_lot.xml",
        "views/product_views.xml",
        "views/stock_location.xml",
        
    ],
    "installable": True,
}
