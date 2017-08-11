# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields, _
import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    @api.depends('chained_discount')
    def _compute_discount(self):
        if self.chained_discount:
            splited_discount = self.chained_discount.split('+')
            disc = 0.00
            for val in splited_discount:
                disc += float(val)
            self.discount = disc
        else:
            self.dicount = 0

    discount = fields.Float(string='Discount (%)',
                            digits=dp.get_precision('Discount'),
                            default=0.0,
                            compute='_compute_discount',
                            store=True)
    chained_discount = fields.Char('Chained Discount', default='0.00')

    @api.model
    def validate_chained_discount(self, discount_str):
        splited_discount = discount_str.split('+')
        for val in splited_discount:
            try:
                float(val)
            except:
                return False
        return True

    @api.onchange('chained_discount')
    def onchange_chained_discount(self):
        valid = self.validate_chained_discount(self.chained_discount)
        if not valid:
            msg = _("Format must be something like 10.5 or 10.5+2+3.4 etc \
                    No strings or ',' allowwed")
            self.chained_discount = '0.00'
            return {'warning': {'title': 'Warning',
                                'message': msg}}
