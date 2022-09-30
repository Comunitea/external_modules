# © 2022 Comunitea (javier@comunitea.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, _
from odoo.exceptions import ValidationError


import logging
_logger = logging.getLogger('REVIEW PAYMENTS WZD: ')


class ReviewPaymentsWzd(models.TransientModel):
    """
    This wizard search for payments not concilied or linked to an invoice
    when it should.
    """
    _name = "review.payments.wzd"
    _description = "Review Payments wizard"

    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 readonly=True,
                                 default=lambda self: self.env.company)
    cancel_payments = fields.Boolean('Cancel break payments')


    def action_confirm(self):
        domain = [
            ('company_id', '=', self.company_id.id),
            ('partner_id', '!=', False),
            ('payment_transaction_id', '=', False),  # Los paypal o redsys de la web pueden no tener factura aun
            ('state', 'in', ('posted', 'reconciled'))
        ]
        # payments = self.env['account.payment'].sudo().search(domain)
        payments = self.env['account.payment'].search(domain)

        len_payments = len(payments)
        idx = 0

        break_payments = self.env['account.payment']
        for pay in payments:
            idx += 1
            _logger.info("***********************************************")
            _logger.info(pay.name)
            msg = "{} / {}".format(idx, len_payments)
            _logger.info(msg)
            _logger.info("***********************************************")

            if pay.reconciled_invoices_count >= 1:
                continue
            break_payments |= pay 

        if not break_payments:
            raise ValidationError(_('Not break payments found'))


        if self.cancel_payments:
            break_payments.action_draft()
            break_payments.cancel()

        action = self.env.ref('account.action_account_payments').read()[0]
        if len(break_payments) > 1:
            action['domain'] = [('id', 'in', break_payments.ids)]
        elif len(break_payments) == 1:
            form_view = [(self.env.ref('account.view_account_payment_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view 
            else:
                action['views'] = form_view
            action['res_id'] = break_payments.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
        
