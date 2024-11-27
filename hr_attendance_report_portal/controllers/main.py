import binascii

from odoo.http import request
from odoo import http, _, fields
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict


class PortalAccount(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        # hr.employee.attendance.report
        if 'attendance_report_count' in counters:
            attendance_report_count = request.env['hr.employee.attendance.report'].search_count(self._get_attendance_reports_domain()) \
                if request.env['hr.employee.attendance.report'].check_access_rights('read', raise_exception=False) else 0
            values['attendance_report_count'] = attendance_report_count

        return values

    def _attendance_report_get_page_view_values(self, attendance_report, access_token, **kwargs):
        values = {
            'page_name': 'Attendance Report',
            'attendance_report': attendance_report,
        }
        return self._get_page_view_values(attendance_report, access_token, values, 'my_attendance_report_history', False, **kwargs)

    def _get_attendance_reports_domain(self):
        return [('employee_id.user_id', '=', request.env.user.id)]

    @http.route(['/my/attendance_reports', '/my/attendance_reports/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_attendance_reports(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        ReportAttendance = request.env['hr.employee.attendance.report']

        domain = self._get_attendance_reports_domain()

        searchbar_sortings = {
            'from_date': {'label': _('Date'), 'order': 'from_date desc'},
            'to_date': {'label': _('Date'), 'order': 'to_date desc'},
        }
        # default sort by order
        if not sortby:
            sortby = 'from_date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [
                ('from_date', '>=', date_begin),
                ('from_date', '<=', date_end),
                ('to_date', '>=', date_begin),
                ('to_date', '<=', date_end)
            ]

        # count for pager
        attendance_report_count = ReportAttendance.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/attendance_reports",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=attendance_report_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        attendance_reports = ReportAttendance.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_attendance_report_history'] = attendance_reports.ids[:100]

        values.update({
            'date': date_begin,
            'attendance_reports': attendance_reports,
            'page_name': 'attendance_report',
            'pager': pager,
            'default_url': '/my/attendance_reports',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("hr_attendance_report_portal.portal_my_attendance_reports", values)

    @http.route(['/my/attendance_reports/<int:attendance_report>'], type='http', auth="public", website=True)
    def portal_my_attendance_reports_detail(self, attendance_report=None, access_token=None, **kw):
        try:
            attendance_report_sudo = self._document_check_access('hr.employee.attendance.report', attendance_report, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._attendance_report_get_page_view_values(attendance_report_sudo, access_token, **kw)

        if attendance_report_sudo.company_id:
            values['res_company'] = attendance_report_sudo.company_id

        return request.render("hr_attendance_report_portal.portal_attendance_report_page", values)

    @http.route(['/my/attendance_reports/<int:attendance_report>/accept'], methods=["POST"], type='json', auth="public", website=True)
    def portal_my_attendance_reports_sign(self, attendance_report, access_token=None, name=None, signature=None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            attendance_report_sudo = self._document_check_access('hr.employee.attendance.report', attendance_report, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid attendance report.')}

        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            attendance_report_sudo.write({
                'signed_by': name,
                'signed_date': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error):
            return {'error': _('Invalid signature data.')}

        query_string = '&message=sign_ok'
        if attendance_report_sudo:
            attendance_report_sudo._action_print_report_and_mail()

        return {
            'force_refresh': True,
            'redirect_url': attendance_report_sudo.get_portal_url(query_string=query_string),
        }
