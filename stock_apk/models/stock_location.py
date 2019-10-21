# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = "stock.location"

    short_name = fields.Char("Short name")
    parent_view_location_id = fields.Many2one('stock.location', help="First location with usage different", compute="get_parent_view_location_id")
    need_package = fields.Boolean()
    need_check= fields.Boolean()
    need_dest_check = fields.Boolean()



    @api.model
    def get_apk_vals(self, type='normal'):
        if not self:
            return False
        vals = {'id': self.id,
                'name': self.short_name or self.display_name}

        if type != 'min':
            vals.update({'barcode': self.barcode,
                         'need_package': self.need_package,
                         'need_check': self.need_check,
                         'need_dest_check': self.need_dest_check})
        if type =='form':
            vals.update({})
        return vals

    @api.multi
    def get_parent_view_location_id(self):
        for location in self:
            usage = location.usage
            if location.usage == 'view':
                location.parent_view_location_id = location
            elif location.location_id.usage != usage or location.location_id.usage == 'view':
                location.parent_view_location_id = location.location_id
            else:
                location.parent_view_location_id = location.parent_view_location_id