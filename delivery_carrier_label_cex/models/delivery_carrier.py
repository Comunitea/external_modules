# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    carrier_type = fields.Selection(selection_add=[('cex', 'Correos Express')])
