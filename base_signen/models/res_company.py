# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ResCompany(models.Model):

    _inherit = 'res.company'

    signen_sign = fields.Binary('Company Signature')
    signen_biometry = fields.Binary('Signature biometry')
