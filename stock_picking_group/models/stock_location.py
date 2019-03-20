# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class StockLocation(models.Model):

    _inherit = 'stock.location'


    def _get_location_type_id(self):
        ##DEVUELVE LA 1ª UBICACIÓN PADRE QUE TENGA PICKING TYPE.
        ## ASI PDRÉ AGRUPAR PICKINGS POR UBICACIONES POR DEBAJO DE LA PADRE (DE STOCK)

        p_loc = self

        while not p_loc.picking_type_id and p_loc.location_id:
            p_loc = p_loc.location_id
        return p_loc

    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type')


