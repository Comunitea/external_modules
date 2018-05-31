# -*- coding: utf-8 -*-
# Copyright 2018 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    received_issued = fields.Boolean('Received / Issued', default=False)
