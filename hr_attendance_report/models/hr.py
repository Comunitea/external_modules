from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    ccc = fields.Char("CCC")
