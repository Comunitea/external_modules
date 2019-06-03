# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class StockPickingType(models.Model):

    _inherit = "stock.picking.type"

    grouped = fields.Boolean('Grouped pick', help="Picked manually created from moves")
    grouped_field_ids = fields.Many2many('ir.model.fields', domain=[('model_id.model', '=', 'stock.move')])

class StockPicking(models.Model):

    _inherit = "stock.picking"

    grouped = fields.Boolean('Grouped pick', help="Picked manually created from moves")
    grouped_close = fields.Boolean('Grouped close', default=False, help='If true, no allow to add moves')


    def get_grouped_close(self):
        return False

    def action_toggle_is_locked(self):
        super().action_toggle_is_locked()
        if self.is_locked:
            self.grouped_close = True
        else:
            self.grouped_close = self.get_grouped_close()
        return True


