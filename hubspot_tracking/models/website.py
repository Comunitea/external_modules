# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class Website(models.Model):

    _inherit = 'website'

    hubspot_url = fields.Char('Hubspot script url')


class WebsiteConfig(models.Model):

    _inherit = 'website.config.settings'


    hubspot_url = fields.Char('Hubspot script url',
                                   related='website_id.hubspot_url')
