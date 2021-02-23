import logging

from odoo import api, fields, models, _

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    computed = fields.Boolean("Computed", default=False)

    @api.model
    def compute_orderpoint_quantities(self, orderpoints=False):
        """
            To override for each module that will use this composer.
        """
        if not orderpoints:
            orderpoints = self.search([('computed', '=', True)])

        for orderpoint in orderpoints:
            if not orderpoint.computed:
                _logger.error('Orderpoint Compute Quantities: This procurement \
                               is not configured to be computed.')
                raise UserError(_('This procurement is not configured \
                                to be computed.'))
            value = (orderpoint.product_id.twelve_months_ago / 365) * 0.2 + \
                    (orderpoint.product_id.six_months_ago / 180) * 0.5 + \
                    (orderpoint.product_id.last_month_ago / 30) * 0.3
            min_qty = value * orderpoint.lead_days
            max_qty = min([min_qty * 2, value * 30])
            orderpoint.write({
                "product_min_qty": min_qty,
                "product_max_qty": max_qty,
            })
            _logger.info('Orderpoint Compute Quantities - Computed Orderpoint \
                          %s with product %s: ' % (
                orderpoint.name, orderpoint.product_id.name)
            )
            _logger.info('Orderpoint Compute Quantities - Computed Product \
                           Min Qty %s and Product Max Qty %s' % (
                orderpoint.product_id.product_min_qty,
                orderpoint.product_id.product_max_qty)
            )

    def button_compute_orderpoint_quantities(self):
        self.compute_orderpoint_quantities(self)

    @api.model
    def _cron_compute_orderpoints(self):
        self.compute_orderpoint_quantities()
