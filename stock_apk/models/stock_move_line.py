# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, models, fields
from pprint import pprint


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'

    default_code = fields.Char(related="product_id.default_code")
    barcode = fields.Char(related="product_id.barcode")

    @api.model
    def get_component_info(self, model_id, model='stock.move.line'):
        move_line = self.browse(model_id)
        product = move_line.product_id
        location = move_line.location_id
        location_dest = move_line.location_dest_id


        if location_dest:
            location_dest_id = {
                '0':  location_dest.id,
                '1':  location_dest.name
            }
        else:
            location_dest_id = False
        
        if move_line.package_id:
            package_id = {
                '0': move_line.package_id.id,
                '1': move_line.package_id.name
            }
        else:
            package_id = False
        
        if move_line.result_package_id:
            result_package_id = {
                '0': move_line.result_package_id.id,
                '1': move_line.result_package_id.name
            }
        else:
            result_package_id = False
        
        if move_line.picking_id:
            picking_id = {
                '0': move_line.picking_id.id,
                '1': move_line.picking_id.name
            }
        else:
            picking_id = False


        data = {
            'id': move_line.id,
            'barcode': location.barcode,
            'barcode_dest': location_dest.barcode,
            'default_code': product.default_code,
            'display_name': product.product_tmpl_id.display_name,
            'final_location_short_name': location_dest.short_name,
            'original_location_short_name': location.short_name,
            'location_dest_id': location_dest_id,
            'location_id': location_dest_id,
            'lot_id': move_line.lot_id.id,
            'lot_name': move_line.lot_name,
            'model': model,
            'move_id': {
                '0': move_line.move_id.id,
                '1': move_line.move_id.name
            },
            'need_check': location.need_check,
            'need_dest_check': location_dest.need_dest_check,
            'ordered_qty': move_line.ordered_qty,
            'package_id': package_id,
            'result_package_id': result_package_id,
            'picking_id': picking_id,
            'product_barcode': product.barcode,
            'product_id': {
                '0': product.id,
                '1': product.name
            },
            'product_need_check': product.need_check,
            'product_qty': move_line.product_qty,
            'product_short_name': product.short_name,
            'product_uom_qty': move_line.product_uom_qty,
            'qty_done': move_line.qty_done,
            'state': move_line.state
        }
        return data
