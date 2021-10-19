# © 2021 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from collections import OrderedDict
from operator import itemgetter

from odoo import http, _, SUPERUSER_ID
from odoo.tools import config
from odoo.exceptions import AccessError, MissingError, AccessDenied
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.l10n_es_aeat_mod347.controllers.main import Mod347Controller
from odoo.addons.web.controllers.main import Home, ensure_db
from odoo.tools import groupby as groupbyelem
from datetime import date, datetime, timedelta

from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        values['mod_347_count'] = request.env['l10n.es.aeat.mod347.partner_record'].search_count(
            [('partner_id', 'child_of', request.env.user.partner_id.commercial_partner_id.id)])
        return values

    @http.route(['/my/347', '/my/347/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_347_list(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Mod347 = request.env['l10n.es.aeat.mod347.partner_record']
        domain = []

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('l10n.es.aeat.mod347.partner_record', domain)

        mod_347_count = Mod347.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/347",
            total=mod_347_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        mod_347_records = Mod347.search(domain, order='report_year desc', limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'mod_347_records': mod_347_records,
            'page_name': '347',
            'archive_groups': archive_groups,
            'default_url': '/my/347',
            'pager': pager,
        })
        return request.render("portal_aeat_mod_347.portal_my_347_list", values)

    def _347_get_page_view_values(self, mod_347_detail, access_token, **kwargs):
        values = {
            'page_name': '347',
            'mod_347_detail': mod_347_detail,
        }
        return self._get_page_view_values(mod_347_detail, access_token, values, 'my_347_history', False, **kwargs)

    @http.route(['/my/347_detail/<int:mod_347_record>'], type='http', auth="public", website=True)
    def portal_347_detail(self, mod_347_record=None, access_token=None, report_type=None, download=False, **kw):
        try:
            mod_347_sudo = self._document_check_access('l10n.es.aeat.mod347.partner_record', mod_347_record, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=mod_347_sudo, report_type=report_type, report_ref='l10n_es_aeat_mod347.report_347_partner', download=download)
        values = self._347_get_page_view_values(mod_347_sudo, access_token, **kw)
        return request.render("portal_aeat_mod_347.portal_347_detail", values)


class Mod347ControllerCustom(Mod347Controller):

    @http.route()
    def mod347_accept(self, res_id, token):
        res = super().mod_347_accept(res_id, token)
        if request.env.user.has_group('base.group_portal'):
            return request.redirect('/my/347_detail/{}'.format(res_ud))
        return res

    @http.route()
    def mod347_reject(self, res_id, token):
        res = super().mod347_reject(res_id, token)
        if request.env.user.has_group('base.group_portal'):
            return request.redirect('/my/347_detail/{}'.format(res_ud))
        return res
