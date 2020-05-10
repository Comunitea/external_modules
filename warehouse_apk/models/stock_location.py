# -*- coding: utf-8 -*-


from odoo import api, models, fields


class StockLocation(models.Model):
    _name = 'stock.location'
    _inherit = ['info.apk', 'stock.location']

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.name

    def get_location_from_apk_values(self, barcode, move_id= False):
        if barcode:
            if len(barcode)==5:
                location = self.search([('barcode', 'ilike', '{}00'.format(barcode))], limit=1)
            else:
                location = self.search([('barcode', '=', barcode)], limit=1)
        if not location and move_id:
            location = move_id.active_location_id ##or move_id[move_id.default_location] or self.env['stock.location']
        return location

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.name

    def return_fields(self, mode='tree'):
        return ['id', 'name', 'usage', 'barcode']

    @api.multi
    def update_stock_location(self):

        for loc in self.search([('usage', '=', 'internal')]):
            print (loc.name)
            loc.barcode = loc.name