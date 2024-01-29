# © 2023 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Virtual Tracking",
    "version": "15.0.0.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "author": "Comunitea, ",
    "depends": [
        "mrp",
        "sale_stock",
        
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_move.xml",
        "views/stock_move_line.xml",
        "views/stock_picking.xml",
        "views/stock_picking_type.xml",
        "views/stock_lot.xml",
        "views/product_views.xml",
        "views/stock_location.xml",
    ],
    "installable": True,
}
