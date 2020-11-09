# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields, _
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def clear_existing_promotion_lines(self):
        res = super(SaleOrder, self).clear_existing_promotion_lines()
        self.order_line.filtered('promotion_line').write({'chained_discount': '0.00'})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    @api.depends('chained_discount')
    def _compute_discount(self):
        # if not self.chained_discount:
        #     self.discount = 0.0
        #     return
        # splited_discount = self.chained_discount.split('+')
        # disc = 0.00
        # for val in splited_discount:
        #     disc += float(val)
        # self.discount = disc
        if self.chained_discount:
            splited_discount = self.chained_discount.split('+')
            disc = 0.00
            cum_disc = 1
            for val in splited_discount:
                cum_disc = cum_disc * (1 - float(val)/100)
                #disc += float(val)
            self.discount = (1- cum_disc) * 100
        else:
            self.discount = 0

    discount = fields.Float(string='Discount (%)',
                            digits=dp.get_precision('Discount'),
                            default=0.0,
                            compute='_compute_discount',
                            store=True)
    chained_discount = fields.Char('Chained Discount', default='0.00')

    @api.model
    def validate_chained_discount(self, discount_str):
        try:
            splited_discount = discount_str.split('+')
            for val in splited_discount:
                float(val)
        except:
            return False
        return True

    @api.onchange('chained_discount')
    def onchange_chained_discount(self):
        if not self.chained_discount:
            self.chained_discount = '0.00'
        valid = self.validate_chained_discount(self.chained_discount)
        if not valid:
            msg = _("Format must be something like 10.5 or 10.5+2+3.4 etc \
                    No strings or ',' allowwed")
            self.chained_discount = '0.00'
            return {'warning': {'title': 'Warning',
                                'message': msg}}

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty',
                  'tax_id')
    def _onchange_discount(self):
        super(SaleOrderLine, self)._onchange_discount()
        if self.discount > 0:
            self.chained_discount = str(self.discount)

    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update({'chained_discount': self.chained_discount})
        return res
