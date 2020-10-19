# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare

class StockProductionLot(models.Model):
    _inherit ="stock.production.lot"

    def find_or_create_lot(self, lot_name, product_id, create):
        lot_id = self.env['info.apk'].get_apk_lot(lot_name.upper(), product_id)
        if not lot_id:
            if not create:
                raise ValidationError ('El nº de serie {} no existe. Debes utilizar nº de serie existentes.')
            sql = "select * from stock_production_lot where name = {}".format(lot_name.upper())
            self._cr.execute(sql)
            if self._cr.fetchall():
                raise ValidationError ('La pda no permite crear números de serie duplicados. Deberás anular los números de serie')
            val = {'name': lot_name.upper(), 'product_id': product_id.id}
            lot_id = self.create(val)
        return lot_id

    def is_enough_to_change(self, location_id, need_qty, strict=True):
        ## Compruebo si me llega la cantidad
        product_id = self.product_id
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        quants = self.env['stock.quant']._gather(product_id=product_id,
                                                 location_id=location_id,
                                                 lot_id=self,
                                                 strict=strict).filtered(lambda quant: float_compare(quant.quantity - quant.reserved_quantity, need_qty, precision_digits=precision_digits) >= 0)
        return quants

    def compute_location_id(self):
        domain = [('quantity', '>', 0), ('lot_id', '=', self.id)]
        return self.env['stock.quant'].search(domain, limit=1).location_id