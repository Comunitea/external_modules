# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PrestashopBackend(models.Model):

    _inherit = 'prestashop.backend'

    invoice_report_folder = fields.Char()
