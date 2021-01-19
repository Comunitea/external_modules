# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class StockQuantPackage(models.Model):

    _inherit = "stock.quant.package"

    partner_id = fields.Many2one('res.partner', string='Delivery Address')