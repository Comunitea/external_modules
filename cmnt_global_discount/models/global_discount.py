# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, _


class GlobalDiscount(models.Model):

    _name = 'global.discount'

    name = fields.Char('Discount Name')
    discount_rate = fields.Float('Discount Rate')
