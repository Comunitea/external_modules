import werkzeug

from odoo import _, http
from odoo.http import request


class BomProductImage(http.Controller):
    
    @http.route('/web/bom_image/<model("product.attribute.value"):value>', type="http", auth="public", website=True)
    def bom_product_image(self, value, **post):
        product_id = value.bom_product_id
        return werkzeug.utils.redirect(
            "/web/image?model=product.product&field=image_128&id={}&write_date={}&unique=1".format(product_id.id, product_id.write_date)
        )