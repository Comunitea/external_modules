# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class StockLocation(models.Model):

    _inherit = 'stock.location'
    _order = "sequence asc"

    ubic = fields.Integer('Secuencia de recorrido', default=0, help="Optional ubication details, for information purpose only")
    inverse_order = fields.Boolean(string='Inverse order', help="Mark for inverse order.")
    sequence = fields.Integer(string='Location order')

    def get_ubic(self):
        return self.get_warehouse().id or self.id

    def get_location_sequence(self):
        if self.usage == 'internal' and self.location_id.usage == 'view':
            return self.location_id.ubic
        else:
            return self.ubic

    @api.multi
    def set_sequence(self):
        for location in self:
            location_sequence = location.get_location_sequence()
            if location.inverse_order:
                posx = 99 - location.posx
            else:
                posx = location.posx
            sequence = "{:03d}{:02d}{:02d}{:02d}".format(location_sequence, posx, location.posy, location.posz)
            print ("Location : {} >> {}".format(location.display_name, sequence))
            location.sequence = sequence

    @api.multi
    def set_barcode_field(self):
        total = len(self)
        inc = 0
        for location in self:
            wh_code = location.get_location_sequence()
            location.barcode = "{:03d}.{:02d}.{:02d}.{:02d}".format(wh_code, location.posx, location.posy, location.posz)
            inc += 1
            print('{} de {} >> {}: Codigo: {}'.format(inc, total, location.display_name, location.barcode))

    @api.onchange('ubic', 'posx', 'posy', 'posz', 'location_id.ubic', 'usage')
    def onchange_act_barcode(self):
        self.set_barcode_field()

