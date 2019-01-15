# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api, fields


class AccountPaymentOrder(models.Model):

    _inherit = 'account.payment.order'

    not_send_emails = fields.Boolean()

    @api.multi
    def generate_move(self):
        res = super(AccountPaymentOrder, self).generate_move()
        mail_pool = self.env['mail.mail']
        mail_ids = self.env['mail.mail']
        for order in self:
            if order.not_send_emails:
                continue

            for line in order.bank_line_ids:
                if order.payment_type == 'inbound':
                    template = self.env.ref(
                        'account_banking_sepa_mail.payment_order_advise_partner',
                        False)
                if order.payment_type == 'outbound':
                    template = self.env.ref(
                        'account_banking_sepa_mail.payment_order_advise_supplier',
                        False)
                ctx = dict(self._context)
                ctx.update({
                    'partner_id': line.partner_id.id,
                    'partner_email': line.partner_id.email,
                    'partner_name': line.partner_id.name,
                    'obj': line
                })
                mail_id = template.with_context(ctx).send_mail(order.id)
                mail_ids += mail_pool.browse(mail_id)
        if mail_ids:
            mail_ids.send()
        return res
