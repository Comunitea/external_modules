from odoo import _, api, fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    ccc = fields.Char("CCC")
