# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    gd_id = fields.Many2one('global.discount', 'Global Discount')
    discount_rate = fields.Float('Discount Rate',
                                 related='gd_id.discount_rate',
                                 readonly=True)
