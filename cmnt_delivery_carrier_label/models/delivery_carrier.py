# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DeliveryCarrier(models.Model):

    _inherit = 'delivery.carrier'

    account_id = fields.Many2one('carrier.account')
    carrier_type = fields.Selection([])
    carrier_services = fields.One2many('delivery.carrier.service', 'carrier_id')

    def get_tracking_link(self, picking):
        ''' Ask the tracking link to the service provider

        :param picking: record of stock.picking
        :return str: an URL containing the tracking link or False
        '''
        self.ensure_one()
        if hasattr(self, '%s_get_tracking_link' % self.carrier_type):
            return getattr(self, '%s_get_tracking_link' % self.carrier_type)(picking)


class DeliveryCarrierService(models.Model):

    _name = 'delivery.carrier.service'

    name = fields.Char()
    carrier_code = fields.Char()
    carrier_id = fields.Many2one('delivery.carrier')
    auto_apply = fields.Boolean(string='Detect Automatically', help="Apply automatically this carrier service.")
    country_id = fields.Many2one('res.country', string='Country',
        help="Apply only if delivery country match.")
    state_ids = fields.Many2many('res.country.state', domain="[('country_id', '=', country_id)]", string='Federal States')
