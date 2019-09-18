# -*- coding: utf-8 -*-
# Copyright 2018 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def get_apk_vals(self, type='normal'):
        if not self:
            return False
        vals = {'id': self.id,
                'name': self.name}
        return vals