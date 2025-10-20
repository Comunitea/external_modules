# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AcountBankingMandates(models.Model):

    _inherit = "account.banking.mandate"
    _order = "by_default desc, signature_date desc"

    active = fields.\
        Boolean("Active", related="partner_bank_id.active", readonly=True,
                help="This field depends on bank account field value")
    by_default = fields.Boolean("By default")
