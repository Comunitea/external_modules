# -*- coding: utf-8 -*-
import logging

from openerp import http

_logger = logging.getLogger(__name__)


class AppController(http.Controller):

    @http.route(['/warehouse_apk/'], type='http', auth='public')
    def a(self, debug=False, **k):
        return http.local_redirect(
            '/warehouse_apk/static/www/index.html')
