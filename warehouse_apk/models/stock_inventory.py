# -*- coding: utf-8 -*-


from odoo import api, models, fields

class StockInventory(models.Model):
    _inherit = ['stock.inventory']

    @api.model
    def action_validate_apk(self, values):
        inventory_id = self.browse(values.get('inventory_id'))
        inventory_id.action_validate()
        location_id = self.env['stock.location'].browse(values.get('location_id'))
        return location_id.get_model_object()

    @api.model
    def load_eans(self, values):
        inventory_id = self.browse(values.get('inventory_id', False))
        product_id = values.get('product_id', False)
        location_id = values.get('location_id', False)
        ean_ids = values.get('ean_ids', '')
        vals = []
        domain = [('inventory_id', '=', inventory_id.id), ('product_id', '=', product_id), ('location_id', '=', location_id)]
        sil = self.env['stock.inventory.line']
        pre_filter = inventory_id.filter
        pre_product = inventory_id.product_id
        inventory_id.filter = 'product'
        inventory_id.product_id = product_id
        lot_names = []
        if ean_ids:
            ean_ids = values.get('ean_ids').split()
        else:
            ean_ids = []
        for ean in ean_ids:
            if ean in lot_names or not ean:
                continue
            lot_names += ean
            lot_domain = [('product_id', '=', product_id), ('name', '=', ean)]
            lot_id = self.env['stock.production.lot'].search(lot_domain)
            if not lot_id:
                lot_vals = {'product_id': product_id, 'name': ean}
                lot_id = self.env['stock.production.lot'].create(lot_vals)
            line_domain = domain + ['|', ('prod_lot_id', '=', False), ('prod_lot_id', '=', lot_id.id)]
            line_id = sil.search(line_domain, limit=1)
            if not line_id:
                vals = {'product_id': product_id,
                        'location_id': location_id,
                        'inventory_id': inventory_id.id,
                        'prod_lot_id': lot_id.id}
                line_id = sil.create(vals)
                line_id._compute_theoretical_qty()
            else:
                if not line_id.prod_lot_id:
                    line_id.prod_lot_id = lot_id
            line_id.product_qty = 1
        inventory_id.product_id = pre_product
        inventory_id.filter = pre_filter
        values.update(
            active_product=product_id,
            active_location=location_id)
        values.pop('ean_ids')
        return self.env['stock.location'].get_apk_inventory(values)