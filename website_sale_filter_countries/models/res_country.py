# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class ResCountry(models.Model):

    _inherit = 'res.country'

    website_available = fields.Boolean()


class ResCountryState(models.Model):

    _inherit = 'res.country.state'

    website_available = fields.Boolean(default=True)
