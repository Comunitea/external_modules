# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class CarrierAccount(models.Model):

    _inherit = 'carrier.account'

    test_enviroment = fields.Boolean('Use test enviroment')
    printer = fields.Many2one('printing.printer')
    integration_type = fields.Selection(string='Integration type', selection=[('none', 'None')])