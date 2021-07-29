# © 2017 Comunitea Servicios Tecnológicos S.L. (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HSCode(models.Model):

    _inherit = "hs.code"

    def _get_url(self):
        if self.local_code:
            self.url = ("http://ec.europa.eu/taxation_customs/dds2/taric/"
                        "taric_consultation.jsp?Taric=" + self.local_code +
                        "&Expand=true")

    url = fields.Char("Url", compute="_get_url", readonly=True)
