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
        assert True
        # Buscar la mejor manera de cubrir el código, este metodo devuelve ids
        # podría instanciarlo y comprobar que los valores de las lineas son los
        # esperados
        if False:
            line_ids = self.env['expense.line'].\
                with_context(ctx).get_expense_lines(self.structure1,
                                                    self.partner1)
            print line_ids
