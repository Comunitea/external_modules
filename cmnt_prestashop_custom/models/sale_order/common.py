# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models
from odoo.addons.queue_job.job import job
from datetime import timedelta


class SaleOrde(models.Model):

    _inherit = "sale.order"

    prestashop_state = fields.Many2one("sale.order.state")

    def write(self, vals):
        res = super().write(vals)
        for order in self:
            if vals.get("prestashop_state"):
                state = order.prestashop_state
                if state.trigger_cancel:
                    order.invoice_ids.filtered(
                        lambda r: r.state == "draft"
                    ).action_cancel()
                    if order.state == "done":
                        order.action_unlock()
                    order.action_cancel()
        return res


class PrestashopSaleOrder(models.Model):
    _inherit = 'prestashop.sale.order'

    @job(default_channel='root.prestashop')
    def import_orders_since(self, backend, since_date=None, **kwargs):
        """ Prepare the import of orders modified on PrestaShop """
        filters = None
        if since_date:
            filters = {'date': '1', 'filter[date_upd]': '>[%s]' % (since_date)}
        if backend.start_import_date:
            if not since_date:
                filters = {'date': '1'}
            filters['filter[date_add]'] = '>[{}]'.format(backend.start_import_date)
        now_fmt = fields.Datetime.now()
        self.env['prestashop.sale.order'].import_batch(
            backend, filters=filters, priority=5, max_retries=0)
        if since_date:
            filters = {'date': '1', 'filter[date_add]': '>[%s]' % since_date}
        self.env['prestashop.mail.message'].import_batch(backend, filters)

        # substract a 10 second margin to avoid to miss an order if it is
        # created in prestashop at the exact same time odoo is checking.
        next_check_datetime = now_fmt - timedelta(seconds=10)
        backend.import_orders_since = next_check_datetime
        return True
