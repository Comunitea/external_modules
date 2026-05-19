# © 2024 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""
Tests para el wizard ComputeRappelInvoice (facturación de rappels calculados).
"""

from datetime import date

from dateutil.relativedelta import relativedelta

import ast

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestRappelInvoice(TransactionCase):
    """Tests del wizard de facturación de rappels."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.rappel_product = cls.env["product.product"].create(
            {
                "name": "Rappel Invoice Product",
                "type": "service",
                "list_price": 0.0,
            }
        )
        # Asignar cuenta de ingresos al producto
        income_account = cls.env["account.account"].search(
            [
                ("account_type", "=", "income"),
                ("company_ids", "in", cls.env.company.id),
            ],
            limit=1,
        )
        cls.rappel_product.property_account_income_id = income_account

        cls.rappel_type = cls.env["rappel.type"].create(
            {
                "name": "Invoice Type",
                "code": "INV",
                "product_id": cls.rappel_product.id,
            }
        )
        cls.rappel = cls.env["rappel"].create(
            {
                "name": "Rappel Para Facturar",
                "type_id": cls.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 5.0,
                "global_application": True,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Invoice Customer",
                "is_company": True,
            }
        )
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", cls.env.company.id)],
            limit=1,
        )

    def _make_calculated_rappel(self, quantity=100.0):
        """Crea un rappel.calculated para usar en el wizard."""
        return self.env["rappel.calculated"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self.rappel.id,
                "date_start": date.today() - relativedelta(months=1),
                "date_end": date.today() - relativedelta(days=1),
                "quantity": quantity,
            }
        )

    def _run_wizard(self, calculated_ids, group_by_partner=False):
        """Ejecuta el wizard de facturación."""
        wizard = self.env["rappel.invoice.wzd"].with_context(
            active_ids=calculated_ids
        ).create(
            {
                "journal_id": self.journal.id,
                "invoice_date": date.today(),
                "group_by_partner": group_by_partner,
            }
        )
        return wizard.action_invoice()

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------

    # Comprueba que el wizard genera un abono (out_refund) con move_id asignado al rappel.calculated y partner correcto.
    def test_action_invoice_creates_credit_note(self):
        """El wizard crea un abono (out_refund) para el rappel calculado."""
        calc = self._make_calculated_rappel(quantity=100.0)
        result = self._run_wizard([calc.id])

        self.assertIsNotNone(result)
        # El rappel calculado debe tener move_id asignado
        self.assertTrue(calc.move_id)
        self.assertEqual(calc.move_id.move_type, "out_refund")
        self.assertEqual(calc.move_id.partner_id, self.partner)

    # Comprueba que la línea del abono creado tiene price_unit igual al campo quantity del rappel.calculated.
    def test_action_invoice_sets_correct_amount(self):
        """La línea del abono tiene el price_unit igual a rappel.quantity."""
        calc = self._make_calculated_rappel(quantity=250.0)
        self._run_wizard([calc.id])

        line = calc.move_id.invoice_line_ids.filtered(
            lambda l: l.product_id == self.rappel_product
        )
        self.assertTrue(line)
        self.assertAlmostEqual(line.price_unit, 250.0, places=2)

    # Comprueba que intentar facturar un rappel.calculated que ya tiene move_id asignado lanza UserError.
    def test_action_invoice_raises_if_already_invoiced(self):
        """Lanza UserError si el rappel calculado ya tiene factura."""
        calc = self._make_calculated_rappel(quantity=100.0)
        # Primera facturación
        self._run_wizard([calc.id])

        # Segunda facturación del mismo rappel: debe fallar
        with self.assertRaises(UserError):
            self._run_wizard([calc.id])

    # Comprueba que rappels con quantity <= 0 se omiten y, al no crearse ninguna factura, se lanza UserError.
    def test_action_invoice_skips_zero_quantity(self):
        """Rappels con quantity <= 0 se omiten sin crear factura."""
        calc_zero = self._make_calculated_rappel(quantity=0.0)
        with self.assertRaises(UserError):
            # No se crea ninguna factura → dispara "Any invoice created!"
            self._run_wizard([calc_zero.id])
        self.assertFalse(calc_zero.move_id)

    # Comprueba que con group_by_partner=True, dos rappels del mismo cliente se consolidan en un único abono.
    def test_action_invoice_group_by_partner(self):
        """Con group_by_partner, dos rappels del mismo cliente van en un solo abono."""
        calc1 = self._make_calculated_rappel(quantity=100.0)
        calc2 = self._make_calculated_rappel(quantity=150.0)
        self._run_wizard([calc1.id, calc2.id], group_by_partner=True)

        self.assertEqual(calc1.move_id, calc2.move_id)
        self.assertEqual(len(calc1.move_id.invoice_line_ids), 2)

    # Comprueba que sin active_ids en el contexto el wizard no crea nada y lanza UserError (no KeyError).
    def test_action_invoice_without_active_ids(self):
        """Sin active_ids en contexto no falla (bug fix #5: KeyError evitado)."""
        wizard = self.env["rappel.invoice.wzd"].create(
            {
                "journal_id": self.journal.id,
                "invoice_date": date.today(),
                "group_by_partner": False,
            }
        )
        # Sin active_ids en el contexto → no crea nada → UserError esperado
        with self.assertRaises(UserError):
            wizard.action_invoice()

    # Comprueba que el wizard devuelve un dict con clave 'domain' que contiene el id del abono creado.
    def test_action_invoice_returns_action(self):
        """El wizard devuelve una acción de ventana con dominio correcto."""
        calc = self._make_calculated_rappel(quantity=80.0)
        result = self._run_wizard([calc.id])

        self.assertIsInstance(result, dict)
        self.assertIn("domain", result)
        domain = ast.literal_eval(result["domain"])
        self.assertIn(calc.move_id.id, domain[0][2])

    # Comprueba que con group_by_partner=False, rappels de partners distintos generan abonos independientes.
    def test_action_invoice_multiple_partners_separate_invoices(self):
        """Sin group_by_partner, partners distintos generan facturas separadas."""
        partner2 = self.env["res.partner"].create(
            {"name": "Second Customer", "is_company": True}
        )
        calc1 = self._make_calculated_rappel(quantity=100.0)
        calc2 = self.env["rappel.calculated"].create(
            {
                "partner_id": partner2.id,
                "rappel_id": self.rappel.id,
                "date_start": date.today() - relativedelta(months=1),
                "date_end": date.today() - relativedelta(days=1),
                "quantity": 150.0,
            }
        )
        self._run_wizard([calc1.id, calc2.id], group_by_partner=False)

        self.assertTrue(calc1.move_id)
        self.assertTrue(calc2.move_id)
        self.assertNotEqual(calc1.move_id, calc2.move_id)

    # Comprueba que si el producto del tipo de rappel no tiene cuenta de ingresos, se usa la cuenta de su categoría.
    def test_action_invoice_account_fallback_to_category(self):
        """Si el producto no tiene cuenta de ingresos, usa la de la categoría."""
        # Crear producto sin cuenta de ingresos directa
        product_no_account = self.env["product.product"].create(
            {
                "name": "No Account Product",
                "type": "service",
                "list_price": 0.0,
            }
        )
        product_no_account.property_account_income_id = False

        rappel_type2 = self.env["rappel.type"].create(
            {
                "name": "Type No Account",
                "code": "NA",
                "product_id": product_no_account.id,
            }
        )
        rappel2 = self.env["rappel"].create(
            {
                "name": "Rappel No Account",
                "type_id": rappel_type2.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 5.0,
                "global_application": True,
            }
        )
        calc = self.env["rappel.calculated"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel2.id,
                "date_start": date.today() - relativedelta(months=1),
                "date_end": date.today() - relativedelta(days=1),
                "quantity": 50.0,
            }
        )
        # Debe crear la factura usando la cuenta de la categoría del producto
        wizard = self.env["rappel.invoice.wzd"].with_context(
            active_ids=[calc.id]
        ).create(
            {
                "journal_id": self.journal.id,
                "invoice_date": date.today(),
                "group_by_partner": False,
            }
        )
        wizard.action_invoice()
        self.assertTrue(calc.move_id)
        self.assertEqual(calc.move_id.move_type, "out_refund")
