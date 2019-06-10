# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ResourceCalendar(models.Model):

    _inherit = 'resource.calendar'

    reminder_delay = fields.Integer(
        help='Delay time before send the reminder to check in (in minutes)')
