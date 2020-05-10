# -*- coding: utf-8 -*-

from odoo import api, models, fields

from odoo.tools import float_is_zero, float_compare

class StockProductionLot(models.Model):
    _inherit ="stock.production.lot"


    def find_or_create_lot(self, lot_name, product_id):
        domain = [('name', '=', lot_name), ('product_id', '=', product_id.id)]
        lot_id = self.search(domain, limit=1)
        if not lot_id:
            val = {'name': lot_name, 'product_id': product_id.id}
            lot_id = lot_id.create(val)
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
