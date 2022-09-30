from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    payments_count = fields.Integer(string="Payments Count",
                                    compute='_compute_payments_count', readonly=True)

    @api.depends('line_ids')
    def _compute_payments_count(self):
        for move in self:
            if move.is_invoice():
                payments = move.line_ids.filtered(lambda r: r.account_internal_type in (
                    "receivable",
                    "payable",
                ))
                self.payments_count = len(payments)

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for move in self:
            if move.is_invoice():
                for line in move.line_ids:
                    line._compute_payment_mode()
        return res

    def action_view_payments(self):
        payments = self.env['account.move.line'].search([('move_id', '=', self.id)]).filtered(lambda r: r.account_internal_type in (
            "receivable",
            "payable",
        ))
        action = self.env.ref('account_due_list.action_invoice_payments').read()[0]
        if len(payments) > 1:
            action['domain'] = [('id', 'in', payments.ids), ('account_id.internal_type', 'in', [
                'receivable', 'payable']), ('balance', '!=', 0)]
        elif len(payments) == 1:
            form_view = [(self.env.ref('account.view_move_line_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + \
                    [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = payments.id

        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (
            self._name, self.id)
        return action
