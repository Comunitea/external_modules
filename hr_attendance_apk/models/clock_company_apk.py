# -*- coding: utf-8 -*-
# Copyright 2019 Comunitea Servicios Tecnológicos S.L.

import logging
from openerp import api, models, fields, _
from openerp import tools
from datetime import datetime
_logger = logging.getLogger(__name__)

MIN_MINUTE = 0


class ResCompany(models.Model):
    _inherit ="res.company"


    @api.model
    def get_clock_apk(self):
        apk = self.env['clock.company.apk'].search([('company_id', '=', self.id)], limit=1)
        return apk

    @api.multi
    def action_view_clock_company_apk_form(self):
        self.ensure_one()
        action_data = self.env.ref('hr_attendance_apk.action_view_clock_company_apk_form').read()[0]
        action_data['context'] = {'default_company_id': 1}
        action_data['domain'] = [('id', '=', self.id)]

        form_view = self.env.ref('hr_attendance_apk.view_clock_company_apk_form')
        action_data['views'] = [(form_view.id, 'form')]
        action_data['res_id'] = self.id
        print action_data
        return action_data

class ClockCompanyApk(models.Model):
    _name = "clock.company.apk"

    @api.multi
    def _get_image(self):
        for p in self:
            p.image_medium = tools.image_get_resized_images(p.image)['image_medium']
            p.image_small = tools.image_get_resized_images(p.image)['image_small']
        #return dict((p.id, tools.image_get_resized_images(p.image)) for p in self)




    company_id = fields.Many2one('res.company')
    name = fields.Char()
    image = fields.Binary('Image', help='Logo in apk')
    image_medium = fields.Binary('Image medium', compute='_get_image')
    image_small = fields.Binary('Image medium', store=False, compute='_get_image')

    welcome_message = fields.Char("Welcome message")
    logo_color = fields.Char("Logo color")
    contact_phone= fields.Char("Contact phone")
    min_minute = fields.Integer ('Minutes between logs', default=3)
    min_accuracity = fields.Integer('Min. accuraccity', default=100)