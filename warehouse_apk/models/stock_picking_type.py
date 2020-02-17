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



class PickingTypeGroupCode(models.Model):

    _inherit = 'picking.type.group.code'

    app_integrated = fields.Boolean('Show in app', default=False)
    picking_fields = fields.Char('Hide fields in app picking tree view')
    move_fields = fields.Char('Hide fields in app stock moves tree view')
    move_line_fields = fields.Char('Hide fields in app stock move lines tree view')

class StockPickingType(models.Model):

    _inherit = 'stock.picking.type'

    app_integrated = fields.Boolean(related='group_code.app_integrated', store=True)
    picking_fields = fields.Char(related='group_code.picking_fields', store=True)
    move_fields = fields.Char(related='group_code.move_fields', store=True)
    move_line_fields = fields.Char(related='group_code.move_line_fields', store=True)
