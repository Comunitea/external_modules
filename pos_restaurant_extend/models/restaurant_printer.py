# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError

import logging
_logger = logging.getLogger(__name__)


class RestaurantPrinter(models.Model):
    _inherit = 'restaurant.printer'

    print_with_serve_buttons = fields.Boolean(
        string='Print with serve buttons',
        default=False,
    )
