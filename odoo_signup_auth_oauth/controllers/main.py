# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import logging
from openerp import http
from openerp.addons.auth_signup.controllers.main import AuthSignupHome as Home
import openerp
from openerp.addons.web.controllers.main import ensure_db
from openerp.http import request
from openerp.tools.translate import _
import werkzeug.utils


_logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# Controller
# ----------------------------------------------------------


class OAuthLogin(Home):

    # Avoid return provaiders, so in web_auth_signup method of auth_oauth
    # module wil bee the normal beahavioior.

    no_list_providers = False

    def list_providers(self):
        providers = super(OAuthLogin, self).list_providers()
        if self.no_list_providers:
            providers = []
        self.no_list_providers = False
        return providers

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        self.no_list_providers = True
        response = super(OAuthLogin, self).web_auth_signup(*args, **kw)
        return response

    @http.route('/web/login2', type='http', auth="none", website=True)
    def web_login2(self, redirect=None, **kw):
        ensure_db()
        providers = self.list_providers()
        if request.httprequest.method == 'GET' and redirect and \
                request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        values['providers'] = providers
        if not redirect:
            redirect = '/web?' + request.httprequest.query_string
        values['redirect'] = redirect

        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db,
                                               request.params['login'],
                                               request.params['password'])
            if uid is not False:
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = _("Wrong login/password")
        if request.env.ref('odoo_signup_auth_oauth.login22', False):
            return request.render('odoo_signup_auth_oauth.login22', values)
        else:
            # probably not an odoo compatible database
            error = 'Unable to login on database %s' % request.session.db
            return werkzeug.utils.redirect('/web/database/selector?error=%s'
                                           % error, 303)
