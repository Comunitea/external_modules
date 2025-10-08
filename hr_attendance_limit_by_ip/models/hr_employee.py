from odoo import models, fields, _
from odoo.http import request
from odoo.exceptions import UserError
import re


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    allow_remote_check_in = fields.Boolean(
        string="Allow Remote Check-In",
        help="If enabled, the user will be able to check in remotely.",
        default=False,
    )

    def _attendance_action_change(self):
        client_ip = str(request.httprequest.environ['REMOTE_ADDR'])
        allowed_ips = self.env.company.ips_allowed_for_check_in
        ip_allowed = False
        if allowed_ips:
            allowed_ip_list = [ip.strip() for ip in allowed_ips.split('\n') if ip.strip()]
            for ip in allowed_ip_list:
                ip_regex = r'%s' % ip
                if re.match(ip_regex, client_ip):
                    ip_allowed = True
                    break
        if not ip_allowed:
            if not self.allow_remote_check_in:
                raise UserError(_('URL not allowed for attendance check in/out'))
            else:
                res = super()._attendance_action_change()
                if self.attendance_state == 'checked_out':
                    if not res.check_out_latitude_text or not res.check_out_longitude_text:
                        raise UserError(_('You can not check out without location data.'))
                else:
                    if not res.check_in_latitude_text or not res.check_in_longitude_text:
                        raise UserError(_('You can not check in without location data.'))
                return res
        return super()._attendance_action_change()
