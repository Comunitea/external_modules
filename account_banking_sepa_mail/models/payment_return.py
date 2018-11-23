# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PaymentReturn(models.Model):
    _inherit = 'payment.return'

    not_send_emails = fields.Boolean()

    def action_confirm(self):
        res = super(PaymentReturn, self).action_confirm()
        if self.not_send_emails:
            return res
        mail_pool = self.env['mail.mail']
        mail_ids = self.env['mail.mail']
        for partner in self.mapped('line_ids.partner_id'):
            template = self.env.ref(
                'account_banking_sepa_mail.payment_return_advise_partner',
                False)
            ctx = dict(self._context)
            ctx.update({
                'partner_email': partner.email,
                'partner_id': partner.id,
                'partner_name': partner.name,
                'lines': self.line_ids.filtered(
                    lambda r: r.partner_id == partner),
            })
            mail_id = template.with_context(ctx).send_mail(self.id)
            mail_ids += mail_pool.browse(mail_id)
        if mail_ids:
            mail_ids.send()
        return res
