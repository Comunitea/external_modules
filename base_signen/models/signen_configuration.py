# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models
from odoo.addons.queue_job.job import job
from ..tools.signen import Signen


class SignenConfigurationUser(models.Model):

    _name = 'signen.configuration.user'
    _rec_name = 'username'

    username = fields.Char(required=True)
    password = fields.Char(required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True)
    configuration_id = fields.Many2one('signen.configuration', 'Configuration')

    @job
    def signen_create_user(self):
        api_key = self.env['ir.config_parameter'].get_param('signen.api.key')
        with Signen(apikey=api_key, nologin=True) as signen:
            signen.create_user(self.username, self.password)


class SignenConfigurationReport(models.Model):

    _name = 'signen.configuration.report'

    name = fields.Char(required=True)
    model_id = fields.Many2one('ir.model', 'Model', required=True)
    model = fields.Char(related='model_id.model', readonly=True)
    report_id = fields.Many2one(
        'ir.actions.report.xml', 'Report')
    report_type = fields.Selection([('report', 'Report'), ('code', 'execute code')])
    execute_code = fields.Text(default='# Variables:\n# obj:Object, signen_report:report_object')
    report_name = fields.Char(
        'Report Filename',
        help="Name to use for the generated report file (may contain placeholders)\n"
        "The extension can be omitted and will then come from the report type.")
    signed_by_company = fields.Boolean()
