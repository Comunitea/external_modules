# -*- coding: utf-8 -*-
import json
import logging
# import werkzeug.utils

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class TsController(http.Controller):

    @http.route('/ts/web', type='http', auth='user')
    def ts_web(self, debug=False, **k):
        # if user not logged in, log him in
        context = {}
        # ts_sessions = request.env['ts.session'].search([('state', '=', 'opened'), ('user_id', '=', request.session.uid)])
        # if not ts_sessions:
        #     return werkzeug.utils.redirect('/web#action=point_of_sale.action_client_ts_menu')
        # ts_sessions.login()
        context = {
            'session_info': json.dumps(request.env['ir.http'].session_info())
        }
        
        return request.render('telesale.index_ts', qcontext=context)
