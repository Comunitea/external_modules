# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api, _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.multi
    def action_confirm(self):
        exception_msg = ""
        if not self.env.context.get('bypass_risk', False):
            partner = self.partner_id.commercial_partner_id
            date_order = self.date_order and \
                datetime.strptime(
                    self.date_order, DEFAULT_SERVER_DATETIME_FORMAT) or \
                datetime.now()
            end_date = datetime.strptime(
                partner.risk_insurance_end_date + ' 00:00:00',
                DEFAULT_SERVER_DATETIME_FORMAT)
            if partner.risk_insurance_end_date and end_date < date_order:
                exception_msg = _('The risk insurance date is exceded.\n')
        return super(SaleOrder,
                     self.with_context(
                         exception_msg=exception_msg)).action_confirm()
