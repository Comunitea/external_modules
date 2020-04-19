# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice.line"

    no_rappel = fields.Boolean("W/O Rappel")
