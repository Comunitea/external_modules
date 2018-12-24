# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ResPartnerBank(models.Model):

    _inherit = "res.partner.bank"

    active = fields.Boolean("Active", default=True)
