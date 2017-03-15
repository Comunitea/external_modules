# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.tests.common import TransactionCase
import time


class TestExpenseStructure(TransactionCase):

    def setUp(self):
        super(TestExpenseStructure, self).setUp()
        self.rpm = self.env['res.partner']
        self.eem = self.env['expense.structure']
        self.etm = self.env['expense.type']
        self.aac = self.env['account.analytic.account']
        self.aaj = self.env['account.analytic.journal']
        self.at = self.env['account.account.type']
        self.ac = self.env['account.account']
        self.aal = self.env['account.analytic.line']

        self.journal1 = \
            self.env.ref('customer_expense_account.analytic_journal1')

        self.type1 = \
            self.env.ref('customer_expense_account.expense_type1')

        self.type2 = \
            self.env.ref('customer_expense_account.expense_type2')

        self.structure1 = \
            self.env.ref('customer_expense_account.expense_structure1')

        self.partner1 = \
            self.env.ref('customer_expense_account.partner1')

        self.analytic_account1 =  \
            self.env.ref('customer_expense_account.analytic_account1')

        self.journal1 = \
            self.env.ref('customer_expense_account.analytic_journal1')
        self.account_type1 = \
            self.env.ref('customer_expense_account.account_type1')

        self.account1 = \
            self.env.ref('customer_expense_account.account1')
        self.analytic_line1 = \
            self.env.ref('customer_expense_account.analytic_line1')

        ctx = {'active_id': self.partner1.id,
               'active_ids': [self.partner1.id],
               'active_model': 'res.partner'}
        self.wzd = self.env['customer.expense.wzd'].\
            with_context(ctx).create({})

    def test_onchange_sructure_id(self):
        element = self.structure1.element_ids[0]
        self.assertEquals(element.name, 'Analytic type 1')
        element.onchange_expense_type_id()
        self.assertEquals(element.name, element.expense_type_id.name)

    def test_default_get(self):
        year = str(time.strftime("%Y"))
        date_start = year + '-' + '01' + '-' + '01'
        date_end = year + '-' + '12' + '-' + '31'
        ctx = {'active_id': self.partner1.id,
               'active_model': 'res.partner'}
        wzd = self.env['customer.expense.wzd'].\
            with_context(ctx).create({})
        self.assertEquals(wzd.start_date, date_start)
        self.assertEquals(wzd.end_date, date_end)
        self.assertEquals(wzd.company_id.id, self.structure1.company_id.id)

    def test_action_show_print_expense(self):
        res = self.wzd.action_show_expense()
        self.assertEquals(res.get('type', ''), 'ir.actions.act_window')

        res = self.wzd.action_print_expense()
        self.assertEquals(res.get('type', ''), 'ir.actions.report.xml')

    def test_get_expense_lines(self):
        year = str(time.strftime("%Y"))
        date_start = year + '-' + '01' + '-' + '01'
        date_end = year + '-' + '12' + '-' + '31'
        ctx = {'from_date': date_start,
               'to_date': date_end,
               'company_id': 1}
        self.env['account.analytic.default'].create({
            'analytic_id': self.analytic_account1.id,
            'partner_id': self.partner1.id
        })
        t_el = self.env['expense.line'].with_context(ctx)
        line_ids = t_el.get_expense_lines(self.structure1, self.partner1)
        num_line = 0
        for line_id in line_ids:
            num_line += 1
            line_obj = t_el.browse(line_id)
            self._check_expense_line_result(line_obj, num_line)
        self.assertTrue(len(line_ids) > 0)

    def _check_expense_line_result(self, l, num_line):
        """
        Check expense_line against expected results testing all types.
        Expected results using the demo data of this module.
        Sales    Cost    Margin    Cost %    Margin %
        500,00           500,00              100,00
                 50,00   450,00     10,00    90,00
        100,00           550,00              91,67
        600,00
                 50,00              8,33
                         550,00              91,67
        600,00   50,00   550,00     8,33     91,67
        50,00            600,00              92,31
        """
        if num_line == 1:
            self.assertEquals(l.name, 'Analytic type 1')
            self.assertEquals(l.compute_type, 'analytic')
            self.assertEquals(l.sales, '500,00')
            self.assertEquals(l.cost, '')
            self.assertEquals(l.margin, '500,00')
            self.assertEquals(l.cost_per, '')
            self.assertEquals(l.margin_per, '100,00')
        elif num_line == 2:
            self.assertEquals(l.name, 'Ratio element')
            self.assertEquals(l.compute_type, 'ratio')
            self.assertEquals(l.sales, '')
            self.assertEquals(l.cost, '50,00')
            self.assertEquals(l.margin, '450,00')
            self.assertEquals(l.cost_per, '10,00')
            self.assertEquals(l.margin_per, '90,00')
        elif num_line == 3:
            self.assertEquals(l.name, 'Invoice type 1')
            self.assertEquals(l.compute_type, 'invoicing')
            self.assertEquals(l.sales, '100,00')
            self.assertEquals(l.cost, '')
            self.assertEquals(l.margin, '550,00')
            self.assertEquals(l.cost_per, '')
            self.assertEquals(l.margin_per, '91,67')
        elif num_line == 4:
            self.assertEquals(l.name, 'Total Sales')
            self.assertEquals(l.compute_type, 'total_sale')
            self.assertEquals(l.sales, '600,00')
            self.assertEquals(l.cost, '')
            self.assertEquals(l.margin, '')
            self.assertEquals(l.cost_per, '')
            self.assertEquals(l.margin_per, '')
        elif num_line == 5:
            self.assertEquals(l.name, 'Total Cost')
            self.assertEquals(l.compute_type, 'total_cost')
            self.assertEquals(l.sales, '')
            self.assertEquals(l.cost, '50,00')
            self.assertEquals(l.margin, '')
            self.assertEquals(l.cost_per, '8,33')
            self.assertEquals(l.margin_per, '')
        elif num_line == 6:
            self.assertEquals(l.name, 'Total Margin')
            self.assertEquals(l.compute_type, 'total_margin')
            self.assertEquals(l.sales, '')
            self.assertEquals(l.cost, '')
            self.assertEquals(l.margin, '550,00')
            self.assertEquals(l.cost_per, '')
            self.assertEquals(l.margin_per, '91,67')
        elif num_line == 7:
            self.assertEquals(l.name, 'Total General')
            self.assertEquals(l.compute_type, 'total_general')
            self.assertEquals(l.sales, '600,00')
            self.assertEquals(l.cost, '50,00')
            self.assertEquals(l.margin, '550,00')
            self.assertEquals(l.cost_per, '8,33')
            self.assertEquals(l.margin_per, '91,67')
        elif num_line == 8:
            self.assertEquals(l.name, 'Fixed Distribution')
            self.assertEquals(l.compute_type, 'distribution')
            self.assertEquals(l.sales, '50,00')
            self.assertEquals(l.cost, '')
            self.assertEquals(l.margin, '600,00')
            self.assertEquals(l.cost_per, '')
            self.assertEquals(l.margin_per, '92,31')
        elif num_line == 9:
            self.assertEquals(l.name, 'Invoicing Distribution')
            self.assertEquals(l.compute_type, 'distribution')
            # Imposible Know the total invoice of the launched test enviroment
            # We only check line is created
        return
