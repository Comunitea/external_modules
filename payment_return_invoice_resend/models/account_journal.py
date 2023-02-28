# © 2023 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    payment_return_charge = fields.Float(
        'Payment Return Charge (%)', default=3)
    min_charge = fields.Float(
        'Payment Return Min Charge', default=15.0)
