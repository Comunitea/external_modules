# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api
from odoo import report as odoo_report
from odoo.addons.queue_job.job import job
from ..tools.signen import Signen


class SignenSignature(models.Model):

    _name = 'signen.signature'

    partner_id = fields.Many2one('res.partner')
    sign_date = fields.Datetime()
    model = fields.Char('Related Document Model', index=True)
    res_id = fields.Integer('Related Document ID', index=True)
    declined = fields.Boolean()

    def get_receivers_dict(self):
        self.ensure_one()
        return {
            'name': self.partner_id.name,
            'phone_prefix': str(self.partner_id.country_id.phone_code),
            'phone': self.partner_id.phone,
            'email': self.partner_id.email
        }


class SignenModel(models.AbstractModel):

    _name = 'signen.model'

    signen_sended = fields.Boolean(copy=False)
    signen_uploaded = fields.Boolean(copy=False)
    signen_document_id = fields.Char(copy=False)
    signen_document_url = fields.Char(compute='_compute_signen_document_url')
    signen_status = fields.Selection(
        [("0", 'pending'), ("2", 'Signed'), ("4", 'declined signature')],
        default="0", copy=False)
    signen_signatures = fields.One2many(
        'signen.signature', 'res_id',
        domain=lambda self: [('model', '=', self._name)], auto_join=True)

    def _compute_signen_document_url(self):
        for obj in self:
            base_url = 'https://webapp.signen.com/document/sended/'
            if obj.signen_document_id:
                obj.signen_document_url = base_url + obj.signen_document_id
            else:
                obj.signen_document_url = ''

    def get_report(self, signen_report):
        report_name = self.env['mail.template'].render_template(
            signen_report.report_name, signen_report.model_id.model, self.id)
        report_service = signen_report.report_id.report_name
        if signen_report.report_id.report_type in ['qweb-html', 'qweb-pdf']:
            result, format = self.env['report'].get_pdf(
                [self.id], report_service), 'pdf'
        else:
            result, format = odoo_report.render_report(
                self._cr, self._uid, [self.id],
                report_service,
                {'model': signen_report.model_id.model}, self._context)
        if not report_name:
            report_name = 'report.' + report_service
        ext = "." + format
        if not report_name.endswith(ext):
            report_name += ext
        return (report_name, result)

    @job
    def send_to_signen_job(self):
        signen_report = self.env['signen.configuration.report'].search(
            [('model', '=', self._name)], limit=1) # Solo funciona si hay 1 documento configurado por modelo.
        api_key = self.env['ir.config_parameter'].get_param('signen.api.key')
        user = self.env['signen.configuration.user'].search([], limit=1)  # TODO: Tal vez quieran mas de 1 user por compañía?
        with Signen(
                user.username,
                user.password, api_key) as signen:
            report_name, report = self.get_report(signen_report)
            receivers_data = [
                x.get_receivers_dict() for x in self.signen_signatures]
            document_id = signen.upload_file(
                report_name, report, receivers_data)
            self.write({'signen_document_id': document_id,
                        'signen_uploaded': True})

    @job
    def company_signature(self):
        user = self.env['signen.configuration.user'].search([], limit=1)  # TODO: Tal vez quieran mas de 1 user por compañía?
        api_key = self.env['ir.config_parameter'].get_param('signen.api.key')
        with Signen(
                user.username,
                user.password, api_key) as signen:
            signen.send_signature(self.signen_document_id, self.company_id)
        self.with_delay()._check_document_status()

    def send_to_signen(self):
        signen_report = self.env['signen.configuration.report'].search(
            [('model', '=', self._name)], limit=1) # Solo funciona si hay 1 documento configurado por modelo.
        self.with_delay().send_to_signen_job()
        self.signen_signatures.create({
            'model': self._name,
            'res_id': self.id,
            'partner_id': self.partner_id.id
        })
        if signen_report.signed_by_company:
            self.signen_signatures.create({
                'model': self._name,
                'res_id': self.id,
                'partner_id': self.company_id.partner_id.id
            })

        self.signen_sended = True

    @job
    def _check_document_status(self):
        api_key = self.env['ir.config_parameter'].get_param('signen.api.key')
        user = self.env['signen.configuration.user'].search(
            [('company_id', '=', self.company_id.id)], limit=1)  # TODO: Tal vez quieran mas de 1 user por compañía?
        new_status = False
        signature_datas = False
        with Signen(
                user.username,
                user.password, api_key) as signen:
            new_status = signen.file_status(self.signen_document_id)
            if new_status != self.signen_status:
                signature_datas = signen.get_signature_status(
                    self.signen_document_id)
                for signature in self.signen_signatures:
                    sign_date = signature_datas.get(
                        signature.partner_id.email)
                    signature.sign_date = sign_date
                    if new_status == '4' and not sign_date:
                        signature.declined = True
                self.signen_status = new_status
                if new_status == '2':
                    document_content = signen.file_evidences(
                        self.signen_document_id)
                    self.env['ir.attachment'].create({
                        'res_model': self._name,
                        'res_id': self.id,
                        'name': 'Signen evidences',
                        'datas': document_content[0].encode('base64'),
                        'datas_fname': 'evidences_{}.pdf'.format(
                            self.signen_document_id),
                    })
                    self.env['ir.attachment'].create({
                        'res_model': self._name,
                        'res_id': self.id,
                        'name': 'Signen file',
                        'datas': document_content[1].encode('base64'),
                        'datas_fname': 'file_{}.pdf'.format(
                            self.signen_document_id),
                    })
        return new_status, signature_datas

    @api.model
    def cron_check_document_status(self):
        for config in self.env['signen.configuration.report'].search([]):
            pending_obj = self.env[config.model].search(
                [('signen_status', '=', "0"), ('signen_uploaded', '=', True)])
            for obj in pending_obj:
                obj.with_delay()._check_document_status()
