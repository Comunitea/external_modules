# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, _
from odoo.osv import expression

class ProcurementGroup(models.Model):

    _inherit = 'procurement.group'

    def _get_orderpoint_domain(self, company_id=False):

        domain = super(ProcurementGroup, self)._get_orderpoint_domain(
            company_id)
        if self._context.get('categ_ids', False):
            categ_ids = self._context.get('categ_ids', False)
            product_ids = self.env['product.product'].search(
                [('categ_id','in', categ_ids)])

            domain = expression.AND([domain, [('product_id', 'in',
                                               product_ids.ids)]])
        return domain

    @api.model
    def _run_orderpoints_category(self, use_new_cursor=False,
                                  company_id=False):
        # Minimum stock rules
        self.sudo()._procure_orderpoint_confirm(use_new_cursor=use_new_cursor,
                                                company_id=company_id)

