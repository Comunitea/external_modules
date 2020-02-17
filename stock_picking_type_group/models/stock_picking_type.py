# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import json

from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval
from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo.addons.shipping_type.models.info_route_mixin import SHIPPING_TYPE_SEL, DEFAULT_SHIPPING_TYPE, STRING_SHIPPING_TYPE, HELP_SHIPPING_TYPE

PICKING_TYPE_GROUP = [('incoming', 'Incoming'),
                      ('outgoing', 'Outgoing'),
                      ('picking', 'Picking'),
                      ('internal', 'Internal'),
                      ('location', 'Location'),
                      ('reposition', 'Reposition'),
                      ('packaging', 'Palets'),
                      ('other', 'Other')]

class PickingTypeGroupCode(models.Model):

    _name = 'picking.type.group.code'

    code = fields.Char('Codigo', help = "{}".format(PICKING_TYPE_GROUP))
    name = fields.Char('Nombre')
    default = fields.Boolean('Por defecto')
    context = fields.Text('Contexto', help="Contexto que se pasa al abrir este grupo")
    domain = fields.Text('Dominio', help="Dominio que se añade al abrir este dominio")

    def get_default(self):
        return  self.search([('default','=', True)], limit=1)

    @api.model
    def create(self, vals):
        return super().create(vals)


class StockPickingType(models.Model):

    _inherit = 'stock.picking.type'

    group_code = fields.Many2one('picking.type.group.code', string="Code group",
                                 default=lambda self: self.env['picking.type.group.code'].get_default())

