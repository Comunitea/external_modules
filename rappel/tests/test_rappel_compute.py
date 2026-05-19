# © 2024 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""
Tests para el cálculo de rappels: _get_next_period, _get_invoices y compute.
Cubre modos fixed/variable y calc_amount percent/qty.
"""

from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests.common import TransactionCase


class TestRappelCompute(TransactionCase):
    """Tests del cálculo de rappels."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.rappel_product = cls.env["product.product"].create(
            {
                "name": "Rappel Product Compute",
                "type": "service",
                "list_price": 0.0,
            }
        )
        cls.rappel_type = cls.env["rappel.type"].create(
            {
                "name": "Type Compute",
                "code": "COMP",
                "product_id": cls.rappel_product.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Sale Product Compute",
                "type": "service",
                "list_price": 100.0,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Compute Customer",
                "is_company": True,
            }
        )
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", cls.env.company.id)],
            limit=1,
        )
        # Cuenta de ingresos para las líneas de factura
        cls.account_income = cls.env["account.account"].search(
            [
                ("account_type", "=", "income"),
                ("company_ids", "in", cls.env.company.id),
            ],
            limit=1,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_invoice(self, move_type, amount, invoice_date, product=None):
        """Crea y valida una factura/abono."""
        product = product or self.product
        move = self.env["account.move"].create(
            {
                "move_type": move_type,
                "partner_id": self.partner.id,
                "journal_id": self.journal.id,
                "invoice_date": invoice_date,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "name": product.name,
                            "quantity": 1,
                            "price_unit": amount,
                            "account_id": self.account_income.id,
                        },
                    )
                ],
            }
        )
        move.action_post()
        return move

    def _make_rappel(self, calc_mode, calc_amount, fix_qty=None, sections=None):
        """Crea un rappel con los parámetros dados y lo vincula al partner."""
        vals = {
            "name": "Test Rappel",
            "type_id": self.rappel_type.id,
            "qty_type": "value",
            "calc_mode": calc_mode,
            "calc_amount": calc_amount,
            "global_application": True,
        }
        if fix_qty is not None:
            vals["fix_qty"] = fix_qty
        rappel = self.env["rappel"].create(vals)

        if sections:
            for sec in sections:
                self.env["rappel.section"].create(
                    {
                        "rappel_id": rappel.id,
                        "rappel_from": sec["from"],
                        "rappel_until": sec["until"],
                        "percent": sec["percent"],
                    }
                )

        date_start = date.today() - relativedelta(months=2)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": date_start,
                "periodicity": "monthly",
            }
        )
        return rappel, rel

    # ------------------------------------------------------------------
    # Tests _get_next_period
    # ------------------------------------------------------------------

    # Comprueba que _get_next_period con periodicidad mensual calcula inicio y fin correctos (inicio + 1 mes - 1 día).
    def test_get_next_period_monthly(self):
        """_get_next_period con periodicidad mensual calcula correctamente."""
        start = date(2024, 1, 1)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self._make_rappel("fixed", "percent", fix_qty=5.0)[0].id,
                "date_start": start,
                "periodicity": "monthly",
            }
        )
        period = rel._get_next_period()
        self.assertEqual(period[0], start)
        self.assertEqual(period[1], date(2024, 1, 31))

    # Comprueba que _get_next_period con periodicidad trimestral calcula el fin a los 3 meses - 1 día.
    def test_get_next_period_quarterly(self):
        """_get_next_period con periodicidad trimestral."""
        start = date(2024, 1, 1)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self._make_rappel("fixed", "percent", fix_qty=5.0)[0].id,
                "date_start": start,
                "periodicity": "quarterly",
            }
        )
        period = rel._get_next_period()
        self.assertEqual(period[0], start)
        self.assertEqual(period[1], date(2024, 3, 31))

    # Comprueba que si last_settlement_date es posterior a date_start, el período siguiente
    # empieza al día siguiente para evitar solapamiento con el período anterior.
    def test_get_next_period_with_last_settlement(self):
        """Si hay last_settlement_date, el siguiente período empieza al día siguiente (sin solapamiento)."""
        start = date(2024, 1, 1)
        last = date(2024, 2, 1)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self._make_rappel("fixed", "percent", fix_qty=5.0)[0].id,
                "date_start": start,
                "periodicity": "monthly",
                "last_settlement_date": last,
            }
        )
        period = rel._get_next_period()
        # El período siguiente empieza el día DESPUÉS de last_settlement_date
        self.assertEqual(period[0], date(2024, 2, 2))
        self.assertEqual(period[1], date(2024, 3, 1))

    # Comprueba que si date_end es anterior al fin natural del período calculado, se usa date_end como tope.
    def test_get_next_period_capped_by_date_end(self):
        """Si date_end es anterior al final del período calculado, se usa date_end."""
        start = date(2024, 1, 1)
        end = date(2024, 1, 15)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self._make_rappel("fixed", "percent", fix_qty=5.0)[0].id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        period = rel._get_next_period()
        self.assertEqual(period[1], end)

    # Comprueba que _get_next_period devuelve False cuando date_start == date_end (rango de 0 días).
    def test_get_next_period_returns_false_when_equal(self):
        """Retorna False cuando date_start == date_end (rango vacío)."""
        single_day = date(2024, 1, 1)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self._make_rappel("fixed", "percent", fix_qty=5.0)[0].id,
                "date_start": single_day,
                "date_end": single_day,
                "periodicity": "monthly",
            }
        )
        period = rel._get_next_period()
        self.assertFalse(period)

    # ------------------------------------------------------------------
    # Tests _get_invoices
    # ------------------------------------------------------------------

    # Comprueba que _get_invoices devuelve líneas de facturas en estado 'posted' dentro del período.
    def test_get_invoices_finds_posted_invoices(self):
        """_get_invoices localiza facturas validadas en el período."""
        invoice_date = date.today() - relativedelta(months=1, days=2)
        invoice = self._make_invoice("out_invoice", 500.0, invoice_date)

        _, rel = self._make_rappel("fixed", "percent", fix_qty=5.0)
        period = rel._get_next_period()
        products = rel.rappel_id.get_products()
        invoice_lines, refund_lines = rel._get_invoices(period, products)

        self.assertTrue(
            any(line.move_id.id == invoice.id for line in invoice_lines)
        )

    # Comprueba que _get_invoices excluye líneas de factura que tienen no_rappel=True.
    def test_get_invoices_ignores_no_rappel_lines(self):
        """_get_invoices no incluye líneas con no_rappel=True."""
        invoice_date = date.today() - relativedelta(months=1)
        product_no_rappel = self.env["product.product"].create(
            {
                "name": "No Rappel Product",
                "type": "service",
                "list_price": 200.0,
                "no_rappel": True,
            }
        )
        invoice = self._make_invoice("out_invoice", 200.0, invoice_date, product=product_no_rappel)
        # Marcar la línea manualmente como no_rappel
        invoice.invoice_line_ids.write({"no_rappel": True})

        _, rel = self._make_rappel("fixed", "percent", fix_qty=5.0)
        period = rel._get_next_period()
        products = rel.rappel_id.get_products()
        invoice_lines, _ = rel._get_invoices(period, products)

        for line in invoice_lines:
            self.assertFalse(line.no_rappel)

    # Comprueba que _get_invoices retorna facturas y abonos en listas separadas con move_type correcto.
    def test_get_invoices_separates_refunds(self):
        """_get_invoices retorna abonos separados de facturas."""
        invoice_date = date.today() - relativedelta(months=1, days=2)
        self._make_invoice("out_invoice", 500.0, invoice_date)
        self._make_invoice("out_refund", 100.0, invoice_date)

        _, rel = self._make_rappel("fixed", "percent", fix_qty=5.0)
        period = rel._get_next_period()
        products = rel.rappel_id.get_products()
        invoice_lines, refund_lines = rel._get_invoices(period, products)

        self.assertTrue(len(invoice_lines) > 0)
        self.assertTrue(len(refund_lines) > 0)
        for line in invoice_lines:
            self.assertEqual(line.move_id.move_type, "out_invoice")
        for line in refund_lines:
            self.assertEqual(line.move_id.move_type, "out_refund")

    # ------------------------------------------------------------------
    # Tests compute – modo fixed / calc_amount percent
    # ------------------------------------------------------------------

    # Comprueba que en modo fixed+percent con período pasado se crea rappel.calculated con el importe correcto (10% del total neto).
    def test_compute_fixed_percent_past_period(self):
        """
        Modo fixed + percent: crea rappel.calculated con amount correcto
        cuando el período ya pasó.
        """
        # Período pasado: hace 2 meses
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)

        self._make_invoice(
            "out_invoice",
            1000.0,
            start + relativedelta(days=5),
        )
        self._make_invoice("out_refund", 100.0, start + relativedelta(days=5))

        rappel = self.env["rappel"].create(
            {
                "name": "Fixed Percent",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 10.0,
                "global_application": True,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [
                ("partner_id", "=", self.partner.id),
                ("rappel_id", "=", rappel.id),
            ]
        )
        self.assertTrue(calculated)
        # El importe debe ser aprox. 10% del total facturado
        invoice_total = sum(invoice_lines.mapped("price_subtotal")) - abs(sum(refund_lines.mapped("price_subtotal")))
        expected = invoice_total * 10.0 / 100.0
        self.assertAlmostEqual(calculated.quantity, expected, places=2)

    # Comprueba que en modo fixed+percent los abonos se restan del total antes de aplicar el porcentaje (no se suman).
    def test_compute_fixed_percent_deducts_refunds(self):
        """
        Bug fix #4: En modo fixed+percent, los abonos deben RESTARSE,
        no sumarse al total.
        """
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        self._make_invoice("out_invoice", 1000.0, mid)
        self._make_invoice("out_refund", 200.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Fixed Percent Refund",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 10.0,
                "global_application": True,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [
                ("partner_id", "=", self.partner.id),
                ("rappel_id", "=", rappel.id),
            ]
        )
        self.assertTrue(calculated)
        # 10% de (1000 - 200) = 80
        self.assertAlmostEqual(calculated.quantity, 80.0, places=2)

    # Comprueba que en modo fixed+qty, compute() usa directamente fix_qty como importe independientemente del volumen.
    def test_compute_fixed_qty(self):
        """Modo fixed + qty usa el importe fijo directamente."""
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        self._make_invoice("out_invoice", 500.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Fixed Qty",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "qty",
                "fix_qty": 50.0,
                "global_application": True,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [
                ("partner_id", "=", self.partner.id),
                ("rappel_id", "=", rappel.id),
            ]
        )
        self.assertTrue(calculated)
        self.assertAlmostEqual(calculated.quantity, 50.0, places=2)

    # ------------------------------------------------------------------
    # Tests compute – modo variable / percent
    # ------------------------------------------------------------------

    # Comprueba que en modo variable+percent, compute() aplica el % de la sección cuyo rango cubre el total facturado.
    def test_compute_variable_percent_hits_section(self):
        """
        Modo variable + percent: calcula el % de la sección correcta.
        """
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        self._make_invoice("out_invoice", 800.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Variable Percent",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "variable",
                "calc_amount": "percent",
                "global_application": True,
            }
        )
        self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 500.0,
                "rappel_until": 1000.0,
                "percent": 5.0,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [
                ("partner_id", "=", self.partner.id),
                ("rappel_id", "=", rappel.id),
            ]
        )
        self.assertTrue(calculated)
        # 5% de 800 = 40
        self.assertAlmostEqual(calculated.quantity, 40.0, places=2)

    # Comprueba que en modo variable+qty, compute() usa el valor fijo (campo percent) de la sección como importe, no un porcentaje.
    def test_compute_variable_qty_hits_section(self):
        """
        Bug fix #3: Modo variable + qty: rappel.calculated.quantity debe
        ser el valor fijo de la sección (no 0).
        """
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        self._make_invoice("out_invoice", 800.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Variable Qty Section",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "variable",
                "calc_amount": "qty",
                "global_application": True,
            }
        )
        self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 500.0,
                "rappel_until": 1000.0,
                "percent": 75.0,  # importe fijo 75
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [
                ("partner_id", "=", self.partner.id),
                ("rappel_id", "=", rappel.id),
            ]
        )
        self.assertTrue(calculated)
        self.assertAlmostEqual(calculated.quantity, 75.0, places=2)

    # Comprueba que en período activo (tmp_model=True), rappel.current.info.amount es el valor de la sección y no 0.
    def test_compute_variable_qty_current_info_amount_not_zero(self):
        """
        Bug fix #3: rappel.current.info.amount no debe ser 0 en modo
        variable + qty cuando el período aún no ha terminado.
        """
        # Período en curso (aún no pasó)
        start = date.today() - relativedelta(days=10)
        end = date.today() + relativedelta(days=20)

        self._make_invoice(
            "out_invoice",
            800.0,
            date.today() - relativedelta(days=5),
        )

        rappel = self.env["rappel"].create(
            {
                "name": "Variable Qty Current Info",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "variable",
                "calc_amount": "qty",
                "global_application": True,
            }
        )
        self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 500.0,
                "rappel_until": 1000.0,
                "percent": 75.0,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines, tmp_model=True)

        current_info = self.env["rappel.current.info"].search(
            [
                ("partner_id", "=", self.partner.id),
                ("rappel_id", "=", rappel.id),
            ]
        )
        self.assertTrue(current_info)
        # El amount debe ser 75.0, no 0.0
        self.assertAlmostEqual(current_info.amount, 75.0, places=2)

    # Comprueba que si el total no alcanza el rappel_from de ninguna sección, no se crea rappel.calculated.
    def test_compute_variable_no_section_match(self):
        """Si no hay sección que cubra el total, no se crea rappel.calculated."""
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        self._make_invoice("out_invoice", 100.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Variable No Section",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "variable",
                "calc_amount": "percent",
                "global_application": True,
            }
        )
        # Sección empieza en 500, no cubre 100
        self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 500.0,
                "rappel_until": 1000.0,
                "percent": 5.0,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [
                ("partner_id", "=", self.partner.id),
                ("rappel_id", "=", rappel.id),
            ]
        )
        self.assertFalse(calculated)

    # Comprueba que tras llamar a compute() con un período ya cerrado, last_settlement_date queda actualizado al fin del período.
    def test_compute_updates_last_settlement_date(self):
        """Después de compute, last_settlement_date se actualiza al final del período."""
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        self._make_invoice("out_invoice", 500.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Settlement Date",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 5.0,
                "global_application": True,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        self.assertEqual(rel.last_settlement_date, period[1])

    # Comprueba que Rappel.compute_rappel() ejecuta el cálculo global para todos los rappels sin lanzar excepciones.
    def test_compute_rappel_global_method(self):
        """Rappel.compute_rappel() ejecuta sin errores para todos los rappels."""
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        self._make_invoice("out_invoice", 300.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Compute All",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 5.0,
                "global_application": True,
            }
        )
        self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        # No debe lanzar excepciones
        rappel.compute_rappel()

    # ------------------------------------------------------------------
    # Tests _get_next_period – periodicidades adicionales
    # ------------------------------------------------------------------

    # Comprueba que _get_next_period con periodicidad semestral calcula el fin correctamente (6 meses - 1 día).
    def test_get_next_period_semiannual(self):
        """_get_next_period con periodicidad semestral calcula correctamente."""
        start = date(2024, 1, 1)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self._make_rappel("fixed", "percent", fix_qty=5.0)[0].id,
                "date_start": start,
                "periodicity": "semiannual",
            }
        )
        period = rel._get_next_period()
        self.assertEqual(period[0], start)
        self.assertEqual(period[1], date(2024, 6, 30))

    # Comprueba que _get_next_period con periodicidad anual calcula el fin correctamente (12 meses - 1 día).
    def test_get_next_period_annual(self):
        """_get_next_period con periodicidad anual calcula correctamente."""
        start = date(2024, 1, 1)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self._make_rappel("fixed", "percent", fix_qty=5.0)[0].id,
                "date_start": start,
                "periodicity": "annual",
            }
        )
        period = rel._get_next_period()
        self.assertEqual(period[0], start)
        self.assertEqual(period[1], date(2024, 12, 31))

    # Comprueba que si last_settlement_date == date_start (no estrictamente mayor), el período parte desde date_start.
    def test_get_next_period_last_settlement_equals_start(self):
        """Si last_settlement_date == date_start, el período parte de date_start."""
        start = date(2024, 1, 1)
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self._make_rappel("fixed", "percent", fix_qty=5.0)[0].id,
                "date_start": start,
                "periodicity": "monthly",
                "last_settlement_date": start,
            }
        )
        period = rel._get_next_period()
        # last_settlement_date NO es estrictamente mayor, así que usa date_start
        self.assertEqual(period[0], start)

    # ------------------------------------------------------------------
    # Tests _get_invoices – casos de filtrado adicionales
    # ------------------------------------------------------------------

    # Comprueba que _get_invoices no retorna líneas de facturas en estado draft (solo se incluyen las 'posted').
    def test_get_invoices_ignores_draft_invoices(self):
        """_get_invoices no incluye facturas en estado draft."""
        invoice_date = date.today() - relativedelta(months=1, days=1)
        # Crear factura sin validar (draft)
        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "journal_id": self.journal.id,
                "invoice_date": invoice_date,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": self.product.name,
                            "quantity": 1,
                            "price_unit": 300.0,
                            "account_id": self.account_income.id,
                        },
                    )
                ],
            }
        )
        # Dejar en draft: no llamar action_post

        _, rel = self._make_rappel("fixed", "percent", fix_qty=5.0)
        period = rel._get_next_period()
        products = rel.rappel_id.get_products()
        invoice_lines, _ = rel._get_invoices(period, products)

        self.assertFalse(any(line.move_id.id == move.id for line in invoice_lines))

    # Comprueba que _get_invoices no retorna líneas de facturas con fecha fuera del rango del período.
    def test_get_invoices_ignores_out_of_period(self):
        """_get_invoices no incluye facturas fuera del período."""
        # Factura con fecha anterior al inicio del período
        old_date = date.today() - relativedelta(months=4)
        self._make_invoice("out_invoice", 400.0, old_date)

        _, rel = self._make_rappel("fixed", "percent", fix_qty=5.0)
        period = rel._get_next_period()
        products = rel.rappel_id.get_products()
        invoice_lines, _ = rel._get_invoices(period, products)

        for line in invoice_lines:
            self.assertGreaterEqual(line.move_id.invoice_date, period[0])
            self.assertLessEqual(line.move_id.invoice_date, period[1])

    # ------------------------------------------------------------------
    # Tests compute – casos adicionales
    # ------------------------------------------------------------------

    # Comprueba que con qty_type='quantity' el cálculo usa el campo quantity de la línea y no price_subtotal.
    def test_compute_qty_type_quantity(self):
        """qty_type='quantity' usa el campo 'quantity' de la línea, no price_subtotal."""
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        # Factura con 10 unidades a 50 €. price_subtotal=500, quantity=10
        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "journal_id": self.journal.id,
                "invoice_date": mid,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": self.product.name,
                            "quantity": 10,
                            "price_unit": 50.0,
                            "account_id": self.account_income.id,
                        },
                    )
                ],
            }
        )
        move.action_post()

        rappel = self.env["rappel"].create(
            {
                "name": "Variable Qty Type Qty",
                "type_id": self.rappel_type.id,
                "qty_type": "quantity",
                "calc_mode": "variable",
                "calc_amount": "percent",
                "global_application": True,
            }
        )
        self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 5.0,
                "rappel_until": 20.0,
                "percent": 10.0,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [("partner_id", "=", self.partner.id), ("rappel_id", "=", rappel.id)]
        )
        self.assertTrue(calculated)
        # 10% de 10 unidades = 1.0 (no de 500 €)
        self.assertAlmostEqual(calculated.quantity, 1.0, places=2)

    # Comprueba que en modo fixed+percent con total=0 (sin facturas), no se genera ningún rappel.calculated.
    def test_compute_fixed_percent_no_invoices_no_calculated(self):
        """Modo fixed+percent sin facturas no crea rappel.calculated (total=0)."""
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)

        rappel = self.env["rappel"].create(
            {
                "name": "Fixed Percent Empty",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 10.0,
                "global_application": True,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [("partner_id", "=", self.partner.id), ("rappel_id", "=", rappel.id)]
        )
        self.assertFalse(calculated)

    # Comprueba que con período futuro no se crea rappel.calculated y last_settlement_date no se modifica.
    def test_compute_future_period_no_calculated_no_settlement_update(self):
        """Período futuro: no crea rappel.calculated y no actualiza last_settlement_date."""
        start = date.today() + relativedelta(days=1)
        end = date.today() + relativedelta(months=1)

        rappel = self.env["rappel"].create(
            {
                "name": "Future Period",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 5.0,
                "global_application": True,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        period = rel._get_next_period()
        if period:
            products = rappel.get_products()
            invoice_lines, refund_lines = rel._get_invoices(period, products)
            rel.compute(period, invoice_lines, refund_lines)

            calculated = self.env["rappel.calculated"].search(
                [("partner_id", "=", self.partner.id), ("rappel_id", "=", rappel.id)]
            )
            self.assertFalse(calculated)
            self.assertFalse(rel.last_settlement_date)

    # Comprueba que un total exactamente igual a rappel_from de una sección es encontrado y el importe calculado es correcto.
    def test_compute_variable_section_boundary_exact(self):
        """Total exactamente en el límite de una sección es encontrado correctamente."""
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        # Total exactamente 500 (rappel_from de la sección)
        self._make_invoice("out_invoice", 500.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Variable Boundary",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "variable",
                "calc_amount": "percent",
                "global_application": True,
            }
        )
        self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 500.0,
                "rappel_until": 1000.0,
                "percent": 5.0,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [("partner_id", "=", self.partner.id), ("rappel_id", "=", rappel.id)]
        )
        self.assertTrue(calculated)
        # 5% de 500 = 25
        self.assertAlmostEqual(calculated.quantity, 25.0, places=2)

    # Comprueba que si el total supera rappel_until de todas las secciones, se usa la sección de mayor rappel_from como fallback.
    def test_compute_variable_above_last_section_uses_fallback(self):
        """Total por encima de rappel_until usa la sección de mayor rappel_from (fallback)."""
        start = date.today() - relativedelta(months=2)
        end = date.today() - relativedelta(months=1, days=1)
        mid = start + relativedelta(days=5)

        # Total 2000 supera el rappel_until=1000 de la última sección
        self._make_invoice("out_invoice", 2000.0, mid)

        rappel = self.env["rappel"].create(
            {
                "name": "Variable Fallback Section",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "variable",
                "calc_amount": "percent",
                "global_application": True,
            }
        )
        self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 0.0,
                "rappel_until": 500.0,
                "percent": 3.0,
            }
        )
        self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 500.0,
                "rappel_until": 1000.0,
                "percent": 5.0,
            }
        )
        rel = self.env["res.partner.rappel.rel"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": rappel.id,
                "date_start": start,
                "date_end": end,
                "periodicity": "monthly",
            }
        )
        products = rappel.get_products()
        period = rel._get_next_period()
        invoice_lines, refund_lines = rel._get_invoices(period, products)
        rel.compute(period, invoice_lines, refund_lines)

        calculated = self.env["rappel.calculated"].search(
            [("partner_id", "=", self.partner.id), ("rappel_id", "=", rappel.id)]
        )
        self.assertTrue(calculated)
        # El fallback elige la sección con rappel_from más alto que cubre: from=500
        # 5% de 2000 = 100
        self.assertAlmostEqual(calculated.quantity, 100.0, places=2)
