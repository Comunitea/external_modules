# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    gd_id = fields.Many2one('global.discount', 'Global Discount')
    discount_type = fields.Selection([('percent', _('Percentage')),
                                      ('amount', _('Amount'))],
                                     string='Discount Type',
                                     help='Select discount type',
                                     default='percent',
                                     related='gd_id.discount_type',
                                     readonly=True)
    discount_rate = fields.Float('Discount Rate',
                                 related='gd_id.discount_rate',
                                 readonly=True)
