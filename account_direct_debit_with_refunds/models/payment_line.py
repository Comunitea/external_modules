# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos S.L (http://comunitea.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PaymentLine(models.Model):
    _inherit = 'payment.line'

    not_change_date = fields.Boolean("Not change date")

    @api.multi
    def write(self, vals):
        if 'not_change_date' not in vals and vals.get('date', False):
            for line in self:
                if line.not_change_date:
                    del vals['date']

        return super(PaymentLine, self).write(vals)

    @api.multi
    def payment_line_hashcode(self):
        self.ensure_one()
        self.refresh()
        return super(PaymentLine, self).payment_line_hashcode()

