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

    def get_ubic(self):
        return self.get_warehouse().id or self.id

    @api.multi
    def set_barcode_field(self):
        total = len(self)
        inc = 0
        for location in self:
            wh_code = location.get_ubic()
            location.barcode = "{:03d}.{:02d}.{:02d}.{:02d}".format(wh_code, location.posx, location.posy, location.posz)
            inc += 1
            print('{} de {} >> {}: Codigo: {}'.format(inc, total, location.display_name, location.barcode))

    @api.onchange('ubic', 'posx', 'posy', 'posz', 'location_id', 'location_id.ubic')
    def onchange_act_barcode(self):
        self.set_barcode_field()

