# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields, _
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def clear_existing_promotion_lines(self):
        res = super(SaleOrder, self).clear_existing_promotion_lines()
        self.order_line.filtered('promotion_line').write(
            {'chained_discount': '0.00'})
        return res
