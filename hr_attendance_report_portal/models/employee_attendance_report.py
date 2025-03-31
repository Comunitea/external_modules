from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
import base64


class EmployeeAttendanceReport(models.Model):
    _name = 'hr.employee.attendance.report'
    _description = 'Print Attendance Report'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', readonly=True, compute='_compute_name')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    from_date = fields.Date('From', required=True)
    to_date = fields.Date('To', required=True)
    signature = fields.Binary('Signature', tracking=True, readonly=True)
    signed = fields.Boolean('Signed', readonly=True, compute='_compute_signed', store=True)
    signed_by = fields.Char('Signed By', readonly=True)
    signed_date = fields.Date('Signed Date', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', related='employee_id.company_id', store=True)
    line_ids = fields.One2many(
        'hr.employee.attendance.report.line',
        'report_id',
        string='Lines',
        readonly=True,
        compute='_compute_line_ids',
        store=True
    )

    message_follower_ids = fields.One2many(
        compute='_compute_message_follower_ids',
        store=True,
    )

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        partner_id = self.env['res.partner'].search([
            ('id', '=', self.env['ir.config_parameter'].sudo().get_param('hr_attendance_report_portal.company_partner_to_send_id')),
        ])
        if not partner_id:
            partner_id = self.env['res.partner'].search([
                ('id', '=', self.env['ir.config_parameter'].sudo().get_param('hr_attendance_report_portal.partner_to_send_id')),
            ])
        if partner_id:
            kwargs['email_from'] = _("ATTENDANCE REPORT <%s>") % partner_id.email
        return super(EmployeeAttendanceReport, self).message_post(**kwargs)

    @api.model
    def create(self, vals):
        res = super(EmployeeAttendanceReport, self).create(vals)
        for report in res:
            report.message_unsubscribe(partner_ids=report.message_follower_ids.mapped('partner_id').ids)
            report.message_subscribe(partner_ids=report.employee_id.user_id.partner_id.ids)

            report.message_post(
                body=_('%s attendance report has been created, please sign it <a href="%s">here<a>') % (report.name, report.access_url),
                subject=_('Attendance Report Created'),
                attachment_ids=[],
                message_type="email",
                subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment'),
            )

            report._compute_message_follower_ids()
        return res

    @api.depends('employee_id')
    def _compute_message_follower_ids(self):
        for report in self:
            partner = self.env['res.partner'].search([
                ('id', '=', self.env['ir.config_parameter'].sudo().get_param('hr_attendance_report_portal.partner_to_send_id')),
            ])
            partner += report.company_id.partner_to_send_id + report.employee_id.user_id.partner_id
            if partner:
                report.message_unsubscribe(partner_ids=report.message_follower_ids.mapped('partner_id').ids)
                report.message_subscribe(partner_ids=partner.ids)

    def _action_print_report_and_mail(self):
        self.ensure_one()
        report = self.print_report()
        report_act = self.env.ref('hr_attendance_report.action_print_attendance')
        pdf = report_act.with_context(report["context"])._render_qweb_pdf(
            report_act.report_name,
            res_ids=self.employee_id.ids,
            data=report['data']
        )
        data_record = base64.b64encode(pdf[0])

        attachment = self.env['ir.attachment'].create({
            'res_model': self._name,
            'res_id': self.id,
            'datas': data_record,
            'name': _('Attendance Report %s.pdf') % self.name,
            'mimetype': 'application/pdf',
        })
        self.message_post(
            body=_('The Attendance Report has been signed by %s') % self.employee_id.name,
            subject=_('Attendance Report signed'),
            attachment_ids=attachment.ids,
            message_type="email",
            subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment'),
        )

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        for report in self:
            if report.from_date > report.to_date:
                raise ValidationError(_('The start date must be anterior to the end date.'))
            reports = self.env['hr.employee.attendance.report'].search([
                ('employee_id', '=', report.employee_id.id),
                ('from_date', '<=', report.to_date),
                ('to_date', '>=', report.to_date),
                ('id', '!=', report.id),
            ]) + self.env['hr.employee.attendance.report'].search([
                ('employee_id', '=', report.employee_id.id),
                ('from_date', '<=', report.from_date),
                ('to_date', '>=', report.from_date),
                ('id', '!=', report.id),
            ]) + self.env['hr.employee.attendance.report'].search([
                ('employee_id', '=', report.employee_id.id),
                ('from_date', '>', report.from_date),
                ('to_date', '<', report.to_date),
                ('id', '!=', report.id),
            ])
            if reports:
                raise ValidationError(_('There is already a report for the selected period.'))

    @api.depends('signature')
    def _compute_signed(self):
        for report in self:
            report.write({'signed': report.signature and True or False})

    @api.depends('employee_id', 'from_date', 'to_date')
    def _compute_name(self):
        for report in self:
            report.name = _('%s from %s to %s') % (report.employee_id.name, report.from_date, report.to_date)

    def _compute_access_url(self):
        super(EmployeeAttendanceReport, self)._compute_access_url()
        for attendance in self:
            attendance.access_url = '/my/attendance_reports/%s' % (attendance.id)

    def recompute_line_ids(self):
        self.ensure_one()
        self._compute_line_ids()

    @api.depends('employee_id', 'from_date', 'to_date')
    def _compute_line_ids(self):
        for report in self:
            if not report.employee_id or not report.from_date or not report.to_date:
                continue
            report.line_ids = False
            data = {
                'ids': [report.employee_id.id],
                'form': {
                    'from_date': datetime.strftime(report.from_date, "%Y-%m-%d"),
                    'to_date': datetime.strftime(report.to_date, "%Y-%m-%d")
                }
            }
            res = self.env['report.hr_attendance_report.print_attendance']._get_report_values(
                docids=report.employee_id.id,
                data=data
            )
            values = []
            for attendance in res["attendances"][report.employee_id.id]:
                values.append((0, 0, {
                    'day': attendance['day'],
                    'ord_hours': attendance['ord_hours'],
                    'extra': attendance['extra'],
                    'message': attendance['in_out_str']
                }))
            report.write({'line_ids': values})

    def print_report(self):
        self.ensure_one()
        datas = {'ids': [self.employee_id.id]}
        from_date = datetime.strftime(self.from_date, '%Y-%m-%d')
        to_date = datetime.strftime(self.to_date, '%Y-%m-%d')
        res = {'from_date': from_date, 'to_date': to_date, 'attendance_report': self.id}
        datas['form'] = res
        return self.env.ref('hr_attendance_report.action_print_attendance').report_action(self, data=datas)


class EmployeeAttendanceReportLine(models.Model):
    _name = 'hr.employee.attendance.report.line'
    _description = 'Print Attendance Report Line'

    report_id = fields.Many2one('hr.employee.attendance.report', string='Report')
    day = fields.Integer('Day')
    ord_hours = fields.Float('Ordinary Hours')
    extra = fields.Float('Extra Hours')
    message = fields.Char('Message')
