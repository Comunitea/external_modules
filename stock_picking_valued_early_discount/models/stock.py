# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from openerp.addons.decimal_precision import decimal_precision as dp


class StockPicking(models.Model):

    _inherit = "stock.picking"

    early_payment_disc_untaxed = fields.Float(
        'Untaxed Amount E.P.', digits=dp.get_precision('Discount'),
        readonly=True, store=True, compute='_amount_all')
    early_payment_disc_tax = fields.Float(
        'Taxes E.P.', digits=dp.get_precision('Discount'),
        readonly=True, store=True, compute='_amount_all')
    early_payment_disc_total = fields.Float(
        'Total with E.P.', digits=dp.get_precision('Discount'),
        readonly=True, store=True, compute='_amount_all')
    total_early_discount = fields.Float(
        'E.P. amount', digits=dp.get_precision('Discount'),
        readonly=True, store=True, compute='_amount_all')

    @api.multi
    @api.depends('move_lines', 'partner_id')
    def _amount_all(self):
        res = super(StockPicking, self)._amount_all()
        for picking in self:
            if not picking.sale_id.early_payment_discount:
                picking.early_payment_disc_untaxed = picking.amount_untaxed
                picking.early_payment_disc_tax = picking.amount_tax
                picking.early_payment_disc_total = picking.amount_total
            else:
                picking.early_payment_disc_untaxed = picking.amount_untaxed * \
                    (1.0 - (float(picking.sale_id.early_payment_discount or
                            0.0)) / 100.0)
                picking.early_payment_disc_tax = picking.amount_tax * \
                    (1.0 - (float(picking.sale_id.early_payment_discount or
                                  0.0)) / 100.0)
                picking.early_payment_disc_total = picking.amount_total * \
                    (1.0 - (float(picking.sale_id.early_payment_discount or
                                  0.0)) / 100.0)
                picking.total_early_discount = \
                    picking.early_payment_disc_untaxed - picking.amount_untaxed
        return res
