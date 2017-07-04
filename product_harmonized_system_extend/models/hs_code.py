# -*- coding: utf-8 -*-
# © 2017 Comunitea Servicios Tecnológicos S.L. (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class HSCode(models.Model):

    _inherit = "hs.code"

    @api.one
    @api.depends('local_code')
    def _get_url(self):
        if self.local_code:
            self.url = (u"http://ec.europa.eu/taxation_customs/dds2/taric/"
                        u"taric_consultation.jsp?Taric=" + self.local_code +
                        u"&Expand=true")

    url = fields.Char("Url", compute="_get_url", readonly=True)
