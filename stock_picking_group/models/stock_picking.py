# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from operator import itemgetter
from itertools import groupby

class StockPicking(models.Model):

    _inherit = "stock.picking"

    need_force_pick = fields.Boolean('Grouped pick', help="Picked manually created from moves")

