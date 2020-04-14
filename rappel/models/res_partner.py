# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    rappel_ids = fields.One2many('res.partner.rappel.rel', 'partner_id',
                                 'Rappels')
