# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class WebsiteSearch(http.Controller):
    @http.route('/shop/search', csrf=False, auth='public', website=True, type='http', methods=['GET'])
    def suggest_search(self, keywords, **params):
        """
        Search products and categories that match keywords
        :param keywords: search query
        :return: json
        """
        if not keywords:
            return json.dumps([])

        Product = request.env['product.template'].with_context(bin_size=True)

        Category = request.env['product.public.category']
        domain = request.website.sale_product_domain()
        domain += [('name', 'ilike', keywords)]

        products = Product.search(domain, limit=10)
        products = [dict(id=p.id, name=p.name, type='p') for p in products]
        if 'category' in params and params['category']:
            categories = Category.search([('name', 'ilike', keywords)], limit=5) 
            categories = [dict(id=c.id, name=c.name, type='c') for c in categories]
            products = categories + products           
        # _logger.debug(products)
        print(products)
        return json.dumps(products)
        
