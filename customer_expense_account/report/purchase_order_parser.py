# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api
from openerp.exceptions import except_orm
from openerp.tools.translate import _
from datetime import datetime as DT


class ExpenseReportParser(models.AbstractModel):
    """
    """
    _name = 'report.customer_expense_account.customer_expense_report'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report_name = 'customer_expense_account.customer_expense_report'
        if not data:
            raise except_orm(_('Error'),
                             _('You must print it from a wizard'))

        line_objs = {}
        for partner_id in data['lines_dic']:
            partner = self.env['res.partner'].browse(int(partner_id))
            line_ids = data['lines_dic'][partner_id]
            line_objs[partner] = self.env['expense.line'].browse(line_ids)

        start = data.get('start_date', False)
        end = data.get('start_date', False)
        if start:
            start = DT.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")
        if end:
            end = DT.strptime(end, "%Y-%m-%d").strftime("%d/%m/%Y")

        docargs = {
            'doc_ids': [],
            'doc_model': 'res.partner',
            'docs': line_objs.keys(),
            'line_objs': line_objs,
            'structure_name': data.get('structure_name', False),
            'start_date': start,
            'end_date': end
        }
        return report_obj.render(report_name, docargs)
