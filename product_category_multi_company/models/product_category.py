# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductCategory(models.Model):

    _inherit = 'product.category'

    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'product.category'))

    def write(self, vals):
        res = super().write(vals)
        if 'company_id' in vals:
            for category in self:
                if category.child_id:
                    category.child_id.write({'company_id': vals['company_id']})
                if category.parent_id and category.parent_id.company_id and \
                        category.company_id != category.parent_id.company_id:
                    raise UserError(_('The category %s must be in the same \
                        company as the parent category') % category.name)
        return res

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.parent_id and res.parent_id.company_id and \
                res.company_id != res.parent_id.company_id:
            res.company_id = res.parent_id.company_id
        return res
