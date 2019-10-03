# Copyright 2018 Omar Castiñeira Saavedra <omar@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderType(models.Model):

    _inherit = "sale.order.type"

    operating_unit_id = fields.Many2one(
        'operating.unit', 'Operating Unit',
        default=lambda self: self.env['res.users'].operating_unit_default_get()
    )
    invoice_group_method_id = fields.Many2one(
        string='Invoice Group Method',
        comodel_name='sale.invoice.group.method'
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for team in self:
            if (team.company_id and team.operating_unit_id and
                    team.company_id != team.operating_unit_id.company_id):
                raise UserError(_('Configuration error!\n\n'
                                  'The Company in the Sales Order Type and in '
                                  'the Operating Unit must be the same.'))
