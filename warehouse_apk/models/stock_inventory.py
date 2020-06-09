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