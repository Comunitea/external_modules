# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields


class PaymentOrder(models.Model):

    _inherit = "payment.order"

    charge_financed = fields.Boolean(states={'sent': [('readonly', True)],
                                             'rejected': [('readonly', True)],
                                             'done': [('readonly', True)]})

    @api.multi
    def action_sent(self):
        res = super(PaymentOrder, self).action_sent()
        mail_pool = self.env['mail.mail']
        mail_ids = self.env['mail.mail']
        for order in self:
            partners = {}
            for line in order.line_ids:
                if line.partner_id.email:
                    if partners.get(line.partner_id):
                        partners[line.partner_id].append(line)
                    else:
                        partners[line.partner_id] = [line]

            for partner_data in partners:
                template = self.env.ref('account_banking_sepadd_groupby_partner.payment_order_advise_partner', False)
                ctx = dict(self._context)
                ctx.update({
                    'partner_email': partner_data.email,
                    'partner_id': partner_data.id,
                    'partner_name': partner_data.name,
                    'lines': partners[partner_data]
                })
                mail_id = template.with_context(ctx).send_mail(order.id)
                mail_ids += mail_pool.browse(mail_id)

        if mail_ids:
            mail_ids.send()
        return res
