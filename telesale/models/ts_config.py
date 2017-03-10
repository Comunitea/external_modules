# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class TsConfig(models.Model):
    _name = 'ts.config'

    name = fields.Char(string='Telesale Name', index=True, required=False,
                       help="An internal identification of the telesale")

    # Methods to open the POS
    @api.multi
    def open_ui(self):
        assert len(self.ids) == 1, "You can open only one session at a time"
        return {
            'type': 'ir.actions.act_url',
            'url': '/ts/web/',
            'target': 'self',
        }
