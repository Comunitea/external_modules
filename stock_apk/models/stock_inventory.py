# -*- coding: utf-8 -*-
# Copyright 2018 Vicente Gutiérrez, <vicente@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models, fields
from pprint import pprint


class StockInventory(models.Model):

    _inherit = 'stock.inventory'

    original_location_short_name = fields.Char(related='location_id.name')
    original_product_short_name = fields.Char(related='product_id.name')

    @api.model
    def action_create_apk(self, vals):
        res = self.create(vals)
        if res:
            return res.id
        else:
            return 0
    
    @api.model
    def action_start_apk(self, vals):
        inventory = self.env['stock.inventory'].browse(vals)
        if inventory.action_start():
            return True
        else:
            return False

    @api.model
    def action_done_apk(self, vals):
        inventory = self.env['stock.inventory'].browse(vals)
        if inventory.action_done():
            return True
        else:
            return False

    @api.model
    def action_cancel_draft_apk(self, vals):
        inventory = self.env['stock.inventory'].browse(vals)
        inventory.action_cancel_draft()
        return True
        
class StockInventoryLine(models.Model):

    _inherit = 'stock.inventory.line'

    product_barcode = fields.Char(related='product_id.barcode')
    product_default_code = fields.Char(related="product_id.default_code")
    original_location_short_name = fields.Char(related='location_id.name')

    @api.model
    def get_quants_for_line_apk(self, vals):
        self = self.sudo()
        package_id = vals['package']
        for val in vals['lines']:
            inventory_line = self.env['stock.inventory.line'].browse(val)
            quant_line = inventory_line._get_quants()
            quant_line.write({
                'package_id': package_id
            })
            inventory_line.write({
                'package_id': package_id
            })
        return True