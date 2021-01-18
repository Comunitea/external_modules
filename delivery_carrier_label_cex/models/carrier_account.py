# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class CarrierAccount(models.Model):
    _inherit = "carrier.account"

    integration_type = fields.Selection(selection_add=[("cex", "CEX")])
    cex_codRte = fields.Char(string="Correos Express codRte")
    cex_solicitante = fields.Char(string="Correos Express Solicitante")
