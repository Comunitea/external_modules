# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

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

    code = fields.Selection(selection=PICKING_TYPE_GROUP, string='Codigo', help = "{}".format(PICKING_TYPE_GROUP))
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

