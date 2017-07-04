# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    # No coge la traducción
    # max_lines_confirm = fields.\
    #     Integer('Queue order confirm if lines greater than', default=15)

    max_lines_confirm = fields.\
        Integer('Encolar confirmación de pedidos si nº de lineas mayor que', 
                default=15)

    @api.model
    def get_default_max_lines_confirm(self, fields):
        res = {}
        icp = self.env['ir.config_parameter']
        res['max_lines_confirm'] = int(icp.get_param('max_lines_confirm', 15))
        return res

    @api.multi
    def set_max_lines_confirm(self):
        icp = self.env['ir.config_parameter']
        icp.set_param('max_lines_confirm', self.max_lines_confirm)
