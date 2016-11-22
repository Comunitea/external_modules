# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from openerp import models, api, fields
import time


class CustomerExpenseWzd(models.TransientModel):
    _name = 'customer.expense.wzd'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    @api.model
    def default_get(self, fields):
        """
        Overwrited to get the secondary unit to the item line.
        """
        res = super(CustomerExpenseWzd, self).default_get(fields)
        year = str(time.strftime("%Y"))
        date_start = year + '-' + '01' + '-' + '01'
        date_end = year + '-' + '01' + '-' + '12'
        res.update(start_date=date_start, end_date=date_end)
        return res

    @api.multi
    def action_show_expense(self):
        value = self.env['expense.line'].show_expense_lines()
        return value
