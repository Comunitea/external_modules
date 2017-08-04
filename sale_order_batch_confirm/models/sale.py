# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models,fields, api
from odoo.addons.queue_job.job import job


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('progress',
                                             'Confirm in Progress')])

    @job
    @api.multi
    def batch_confirm_one_order(self):
        self.ensure_one()
        ctx = self._context.copy()
        ctx.update({'do_super': True})
        self.with_context(ctx).action_confirm()
        self.env.user.notify_info('The confirmation batch order has finished')

    @api.multi
    def action_confirm(self):
        res = False
        icp = self.env['ir.config_parameter']
        max_lines_len = int(icp.get_param('max_lines_confirm', '15'))
        for order in self:
            if not self._context.get('do_super', False) and \
                    len(order.order_line) >= max_lines_len:
                order.state = "progress"
                res = order.with_delay().batch_confirm_one_order()
                return True
            else:
                res = super(SaleOrder, self).action_confirm()
        return res
