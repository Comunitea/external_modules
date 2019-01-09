# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.tools.float_utils import float_compare, float_round, float_is_zero

class StockQuant(models.Model):

    _inherit = "stock.quant"

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None, strict=False):
        print("Entro en _update_reserved_quantity con {}".format(self._context))
        if self.env.context.get('forced_move_line', False):
            return []
        return super(StockQuant, self)._update_reserved_quantity(product_id=product_id, location_id=location_id, quantity=quantity, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict)


    @api.model
    def _get_available_quantity_by_lot(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False, allow_negative=False):
        """
        COPY _get_available_quantity, devuelvo {} de lotes y cantidades
        RECIBE OBJETOAS, NO IDS
        """
        self = self.sudo()

        quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict)
        rounding = product_id.uom_id.rounding
        if product_id.tracking == 'none':
            available_quantity = sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))
            if allow_negative:
                availaible_quantities = {'untracked': available_quantity}
            else:
                availaible_quantities = {'untracked': available_quantity if float_compare(available_quantity, 0.0, precision_rounding=rounding) >= 0.0 else 0.0}
        else:
            availaible_quantities = {"{}".format(lot_id): 0.0 for lot_id in list(set(quants.mapped('lot_id'))) + ['untracked']}
            for quant in quants:
                if not quant.lot_id:
                    availaible_quantities['untracked'] += quant.quantity - quant.reserved_quantity
                else:
                    availaible_quantities["{}".format(quant.lot_id.id)] += quant.quantity - quant.reserved_quantity

        return availaible_quantities

