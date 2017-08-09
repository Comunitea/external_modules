# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, _

ACTION_ADD = [
    ('chained_discount', _('Chained discounts'))
]


class PromotionsRulesActions(models.Model):
    _inherit = 'promos.rules.actions'

    action_type = fields.Selection(selection_add=ACTION_ADD)

    def action_chained_discount(self, order):
        """
        Crea hasta 4 descuentos, en la misma línea si esta cumple que es un
        pallet,
        cada uno en una columna para las promociones implicadas.
        """
        selected_lines = []
        restrict_codes = False
        if self.product_code:
            restrict_codes = self.product_code.replace("'", '').split(',')
        for line in order.order_line.\
                filtered(lambda l: not l.product_id.no_promo):
            if restrict_codes and line.product_id.code not in restrict_codes:
                continue
            selected_lines += line
        self._create_chained_discounts(selected_lines)

    def _create_chained_discounts(self, selected_lines):
        """
        Crea hasta 4 descuentos, en la misma línea,
        cada uno en una columna para las promociones implicadas.
        """
        discount = eval(self.arguments)
        for line in selected_lines:
            disc_str = line.chained_discount
            if disc_str != '0.00':
                disc_str += "+" + str(discount)
            else:
                disc_str = str(discount)
            line.chained_discount = disc_str
            line.promotion_line = True
        return
