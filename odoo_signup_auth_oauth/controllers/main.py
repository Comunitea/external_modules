# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import logging
from openerp import http
from openerp.addons.auth_signup.controllers.main import AuthSignupHome as Home


_logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# Controller
# ----------------------------------------------------------


class OAuthLogin(Home):

    # Avoid return provaiders, so in web_auth_signup method of auth_oauth
    # module wil bee the normal beahavioior.

    no_list_providers = False

    def list_providers(self, no_return=False):
        providers = super(OAuthLogin, self).list_providers()
        if self.no_list_providers:
            providers = []
        return providers

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        self.no_list_providers = True
        response = super(OAuthLogin, self).web_auth_signup(*args, **kw)
        return response
