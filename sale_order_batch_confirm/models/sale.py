# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, exceptions, _
from odoo.addons.queue_job.job import job


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    @api.depends('order_jobs_ids', 'order_jobs_ids.state')
    def _get_last_job_fail(self):
        for order in self:
            if order.order_jobs_ids:
                last_job = order.order_jobs_ids[-1]
                if last_job.state == 'failed':
                    order.last_job_failed = True

    state = fields.Selection(selection_add=[('progress',
                                             'Confirm in Progress')])
    order_jobs_ids = fields.Many2many(comodel_name='queue.job',
                                      column1='order_id', column2='job_id',
                                      string="Queue orders", copy=False)
    last_job_failed = fields.Boolean('Last confirmation failed',
                                     compute='_get_last_job_fail', store=True)

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
        queue_obj = self.env['queue.job']
        max_lines_len = int(icp.get_param('max_lines_confirm', '15'))
        for order in self:
            if not self._context.get('do_super', False) and \
                    len(order.order_line) >= max_lines_len:
                order.state = "progress"
                ctx = order._context.copy()
                ctx.update(company_id=order.company_id.id)
                order2 = self.with_context(ctx).browse(order.id)
                res = order2.sudo().with_delay().batch_confirm_one_order()
                # Add job to the orders queue
                queue_ids = queue_obj.search([('uuid', '=', res.uuid)],
                                             limit=1)
                order2.sudo().order_jobs_ids |= queue_ids
                return True
            else:
                res = super(SaleOrder, self).action_confirm()
        return res

    @api.multi
    def _cancel_order_jobs(self):
        for queue in self.mapped('order_jobs_ids'):
            if queue.state == 'started':
                return False
            elif queue.state in ('pending', 'enqueued', 'failed'):
                queue.sudo().unlink()
        return True

    @api.multi
    def action_cancel(self):
        for queue in self.mapped('order_jobs_ids'):
            if not self._cancel_order_jobs():
                raise exceptions.\
                    Warning(_('You can not cancel this order because'
                              ' there is a job running!'))
        res = super(SaleOrder, self).action_cancel()
        return res

