# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DeliveryCarrier(models.Model):

    _inherit = 'delivery.carrier'

    account_id = fields.Many2one('carrier.account')
    carrier_type = fields.Selection([])
    carrier_services = fields.One2many('delivery.carrier.service', 'carrier_id')


class DeliveryCarrierService(models.Model):

    _name = 'delivery.carrier.service'

    name = fields.Char()
    carrier_code = fields.Char()
    carrier_id = fields.Many2one('delivery.carrier')
