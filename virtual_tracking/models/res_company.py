# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    serial_to_upper_case = fields.Boolean(
        string='Upper lot/serial names', default=False
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    serial_to_upper_case = fields.Boolean(related="company_id.serial_to_upper_case", readonly=False)
