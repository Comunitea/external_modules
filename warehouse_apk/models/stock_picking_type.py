# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval
from odoo import api, fields, models, _
from datetime import datetime, timedelta
import time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class PickingTypeGroupCode(models.Model):
    _name = 'picking.type.group.code'
    _inherit = ['info.apk', 'picking.type.group.code']



    app_integrated = fields.Boolean('Show in app', default=False)
    tree_picking_fields = fields.Char('Pick fields (tree)')
    tree_move_fields = fields.Char('Move fields (tree)')
    tree_move_line_fields = fields.Char('Move line (tree)')
    form_picking_fields = fields.Char('Pick fields (form)')
    form_move_fields = fields.Char('Move fields (form)')
    form_move_line_fields = fields.Char('Move line fields (form)')
    field_status_apk = fields.Char(string="Estado de campos en PDA", default='0000000',
                               help="Indica el estado binario de los campos en la PDA:\n"
                                              "Producto, Origen, Lote, Paquete, Destino, Paquete Destino y Cantidad\n"
                                              "Con los valores\n "
                                              "Bit 1 - Visible\nBit 2 - Requerido\nBit 3 - Hecho\n"
                                              "Validable cuando bit 3 está a 0")
    default_location = fields.Selection(selection=[('location_id', 'Origen'), ('location_dest_id', 'Destino')], string="Tipo de ubicación por defecto")
    icon = fields.Char("Icono")
    allow_overprocess = fields.Boolean('Overprocess', help="Permitir realizar más cantidad que la reservada")
    def return_fields(self, mode='tree'):
        return ['code', 'name', 'app_integrated', 'icon']

class StockPickingType(models.Model):

    _name = 'stock.picking.type'
    _inherit = ['info.apk', 'stock.picking.type']

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.barcode or obj.name

    app_integrated = fields.Boolean(related='group_code.app_integrated')
    tree_picking_fields = fields.Char(related='group_code.tree_picking_fields')
    tree_move_fields = fields.Char(related='group_code.tree_move_fields')
    tree_move_line_fields = fields.Char(related='group_code.tree_move_line_fields')
    form_picking_fields = fields.Char(related='group_code.form_picking_fields')
    form_move_fields = fields.Char(related='group_code.form_move_fields')
    form_move_line_fields = fields.Char(related='group_code.form_move_line_fields')
    field_status_apk = fields.Char(related="group_code.field_status_apk")
    default_location = fields.Selection(related="group_code.default_location")
    group_code_code = fields.Selection(related="group_code.code", store=True)
    allow_overprocess = fields.Boolean(related='group_code.allow_overprocess')
    def return_fields(self, mode='tree'):

        fields = ['id', 'apk_name', 'color', 'warehouse_id', 'code', 'name', 'count_picking_ready', 'count_picking_waiting',
                  'count_picking_late', 'count_picking_backorders', 'rate_picking_late', 'barcode',
                  'rate_picking_backorders']

        if mode == 'form':
            fields += []
        return fields

    def _compute_picking_count_domains(self):
        # DEBE SER UNA COPIA DE LOS DOMINIOS QUE SE USAN PARA CALCULAR LOS VALORES
        domains = {
            'count_picking_draft': [('state', '=', 'draft')],
            'count_picking_waiting': [('state', 'in', ('confirmed', 'waiting'))],
            'count_picking_ready': [('state', '=', 'assigned')],
            'count_picking': [('state', 'in', ('assigned', 'waiting', 'confirmed'))],
            'count_picking_late': [('scheduled_date', '<', time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)), ('state', 'in', ('assigned', 'waiting', 'confirmed'))],
            'count_picking_backorders': [('backorder_id', '!=', False), ('state', 'in', ('confirmed', 'assigned', 'waiting'))],
        }
        return domains