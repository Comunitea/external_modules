from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    ccc = fields.Char("CCC")
