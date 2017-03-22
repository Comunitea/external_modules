# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# © 2017 El Nogal  - Pedro Gómez <pegomez@elnogal.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api
from openerp.exceptions import except_orm
from openerp.tools.translate import _
from datetime import datetime as dt


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
            partner = self.env['res.partner'].browse(int(partner_id)) \
                if partner_id != 'summary' else False
            line_ids = data['lines_dic'][partner_id][1]
            line_objs[partner] = (data['lines_dic'][partner_id][0], 
                                  self.env['expense.line'].browse(line_ids))
        start = data.get('start_date', False)
        end = data.get('end_date', False)
        summary_description = data.get('summary_description', False)
        if start:
            start = dt.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")
        if end:
            end = dt.strptime(end, "%Y-%m-%d").strftime("%d/%m/%Y")

        docargs = {
            'doc_ids': [],
            'doc_model': 'res.partner',
            'docs': line_objs.keys(),
            'line_objs': line_objs,
            'start_date': start,
            'end_date': end,
            'summary_description': summary_description
        }
        return report_obj.render(report_name, docargs)
