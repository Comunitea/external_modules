# -*- coding: utf-8 -*-
#
# © 2016 Comunitea
# © 2019 Comunitea Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCountry(models.Model):

    _inherit = 'res.country'

    website_available = fields.Boolean(default=False)


class ResCountryState(models.Model):

    _inherit = 'res.country.state'

    website_available = fields.Boolean(default=False)
