# © 2023 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    expense_product_id = fields.Many2one(
        'product.product', 'Returned Payment Expense')
