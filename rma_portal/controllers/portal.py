from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        values['rma_count'] = request.env['rma.order.line'].search_count([])
        return values

    def _rma_get_page_view_values(self, rma, access_token, **kwargs):
        values = {
            'page_name': 'rma',
            'rma': rma,
        }
        return self._get_page_view_values(rma, access_token, values, 'my_rma_history', False, **kwargs)

    @http.route(['/my/rmas', '/my/rmas/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_rmas(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Rma = request.env['rma.order.line']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('rma.order.line', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        # rma count
        rma_count = Rma.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/rmas",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=rma_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        rma = Rma.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_rma_history'] = rma.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'rmas': rma,
            'page_name': 'rma',
            'archive_groups': archive_groups,
            'default_url': '/my/rma',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("rma_portal.portal_my_rmas", values)

    @http.route(['/my/rma/<int:rma_id>'], type='http', auth="public", website=True)
    def portal_my_rma(self, rma_id=None, access_token=None, **kw):
        try:
            rma_sudo = self._document_check_access('rma.order.line', rma_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._rma_get_page_view_values(rma_sudo, access_token, **kw)
        return request.render("rma_portal.portal_my_rma", values)
