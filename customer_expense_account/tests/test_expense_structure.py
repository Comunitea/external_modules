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

        vals = {
            'name': 'Analytic type',
            'compute_type': 'analytic',
        }
        self.type1 = self.etm.create(vals)
        vals = {
            'name': 'Based on parent element',
            'compute_type': 'ratio',
        }
        self.type2 = self.etm.create(vals)

        vals = {
            'name': 'Test Structure 1',
            'element_ids': [(0, 0, {
                'name': 'Element Analytic Type',
                'expense_type_id': self.type1.id
            }), (0, 0, {
                'name': 'Element Analytic Type',
                'expense_type_id': self.type1.id
            })]
        }
        self.structure1 = self.eem.create(vals)

        self.partner1 = self.rpm.create({
            'name': 'Test Partner 1',
            'structure_id': self.structure1.id
        })

    def test_onchange_sructure_id(self):
        element = self.structure1.element_ids[0]
        self.assertEquals(element.name, 'Element Analytic Type')
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
