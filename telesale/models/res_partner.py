# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commercial_partner_name = fields.Char(string='Commercial Name',
                                          related='commercial_partner_id.name')
