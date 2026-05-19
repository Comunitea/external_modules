# © 2024 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from psycopg2.errors import NotNullViolation

class TestRappelBase(TransactionCase):
    """Clase base con datos comunes para todos los tests de rappel."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Producto de rappel (usado para facturar)
        cls.rappel_product = cls.env["product.product"].create(
            {
                "name": "Rappel Product",
                "type": "service",
                "list_price": 0.0,
            }
        )
        cls.rappel_type = cls.env["rappel.type"].create(
            {
                "name": "Rappel Test Type",
                "code": "TEST",
                "product_id": cls.rappel_product.id,
            }
        )

        # Producto de venta normal
        cls.product = cls.env["product.product"].create(
            {
                "name": "Sale Product",
                "type": "service",
                "list_price": 100.0,
            }
        )

        # Cliente
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Customer",
                "is_company": True,
            }
        )

        # Diario de ventas
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", cls.env.company.id)],
            limit=1,
        )


class TestRappelType(TestRappelBase):
    """Tests para RappelType."""

    # Comprueba que el tipo de rappel se crea con los campos nombre, código y producto correctos.
    def test_rappel_type_creation(self):
        """El tipo de rappel se crea correctamente."""
        self.assertEqual(self.rappel_type.name, "Rappel Test Type")
        self.assertEqual(self.rappel_type.code, "TEST")
        self.assertEqual(self.rappel_type.product_id, self.rappel_product)

    # Comprueba que intentar crear un tipo de rappel sin producto lanza NotNullViolation.
    def test_rappel_type_required_product(self):
        """No se puede crear un tipo de rappel sin producto."""
        with self.assertRaises(NotNullViolation):
            self.env["rappel.type"].create(
                {
                    "name": "Sin producto",
                    "code": "SP",
                }
            )


class TestRappelModel(TestRappelBase):
    """Tests para el modelo Rappel y sus secciones."""

    # Comprueba que un rappel con global_application=True se crea correctamente con sus campos.
    def test_rappel_global_creation(self):
        """Rappel global se crea correctamente."""
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel Global",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 5.0,
                "global_application": True,
            }
        )
        self.assertTrue(rappel.global_application)
        self.assertEqual(rappel.fix_qty, 5.0)

    # Comprueba que la constraint impide crear un rappel no global sin producto ni categoría.
    def test_rappel_constraint_no_global_no_product(self):
        """No puede existir un rappel no global sin producto ni categoría."""
        with self.assertRaises(ValidationError):
            self.env["rappel"].create(
                {
                    "name": "Rappel sin aplicación",
                    "type_id": self.rappel_type.id,
                    "qty_type": "value",
                    "calc_mode": "fixed",
                    "calc_amount": "percent",
                    "fix_qty": 5.0,
                    "global_application": False,
                }
            )

    # Comprueba que un rappel no global con product_id definido supera la constraint.
    def test_rappel_by_product(self):
        """Rappel vinculado a producto específico pasa la constraint."""
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel por Producto",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 3.0,
                "global_application": False,
                "product_id": self.product.id,
            }
        )
        self.assertEqual(rappel.product_id, self.product)

    # Comprueba que un rappel no global con product_categ_id definido supera la constraint.
    def test_rappel_by_category(self):
        """Rappel vinculado a categoría pasa la constraint."""
        categ = self.env["product.category"].search([], limit=1)
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel por Categoría",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 2.0,
                "global_application": False,
                "product_categ_id": categ.id,
            }
        )
        self.assertEqual(rappel.product_categ_id, categ)

    # Comprueba que get_products() con global_application=True devuelve todos los productos del sistema.
    def test_get_products_global(self):
        """get_products() con global_application devuelve todos los productos."""
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel Global Prod",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 1.0,
                "global_application": True,
            }
        )
        products = rappel.get_products()
        all_products = self.env["product.product"].search([])
        self.assertEqual(len(products), len(all_products))

    # Comprueba que get_products() con product_id devuelve únicamente ese producto.
    def test_get_products_by_product(self):
        """get_products() con product_id devuelve solo ese producto."""
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel Producto Específico",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 1.0,
                "global_application": False,
                "product_id": self.product.id,
            }
        )
        products = rappel.get_products()
        self.assertEqual(products, [self.product.id])

    # Comprueba que get_products() con product_categ_id devuelve solo los productos de esa categoría.
    def test_get_products_by_category(self):
        """get_products() con product_categ_id devuelve productos de esa categoría."""
        categ = self.product.categ_id
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel Categoría Específica",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 1.0,
                "global_application": False,
                "product_categ_id": categ.id,
            }
        )
        products = rappel.get_products()
        expected = self.env["product.product"].search(
            [("categ_id", "=", categ.id)]
        )
        self.assertEqual(sorted(products), sorted(expected.ids))


class TestRappelSection(TestRappelBase):
    """Tests para RappelSection."""

    # Comprueba que display_name de rappel.section devuelve el string con los valores 'from - until'.
    def test_section_name_get(self):
        """display_name devuelve 'from - until'."""
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel Sections",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "variable",
                "calc_amount": "percent",
                "global_application": True,
            }
        )
        section = self.env["rappel.section"].create(
            {
                "rappel_id": rappel.id,
                "rappel_from": 0.0,
                "rappel_until": 1000.0,
                "percent": 5.0,
            }
        )
        name = section.display_name
        self.assertIn("0.0", name)
        self.assertIn("1000.0", name)


class TestRappelAdviceEmail(TestRappelBase):
    """Tests para RappelAdvices."""

    def _make_rappel(self):
        return self.env["rappel"].create(
            {
                "name": "Rappel Advice",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 5.0,
                "global_application": True,
            }
        )

    # Comprueba que un advice con tipo 'fixed' y cualquier valor de timing se crea sin error.
    def test_advice_timing_fixed_valid(self):
        """Advice con timing fijo se crea sin error."""
        rappel = self._make_rappel()
        advice = self.env["rappel.advice.email"].create(
            {
                "rappel_id": rappel.id,
                "advice_timing": "fixed",
                "timing": 15,
            }
        )
        self.assertEqual(advice.timing, 15)

    # Comprueba que un advice con tipo 'variable' y timing entre 1 y 99 es válido.
    def test_advice_timing_variable_valid(self):
        """Advice con timing variable entre 1 y 99 es válido."""
        rappel = self._make_rappel()
        advice = self.env["rappel.advice.email"].create(
            {
                "rappel_id": rappel.id,
                "advice_timing": "variable",
                "timing": 50,
            }
        )
        self.assertEqual(advice.timing, 50)

    # Comprueba que timing variable = 0 está fuera del rango permitido y lanza ValidationError.
    def test_advice_timing_variable_zero_raises(self):
        """Advice con timing variable = 0 lanza ValidationError."""
        rappel = self._make_rappel()
        with self.assertRaises(ValidationError):
            self.env["rappel.advice.email"].create(
                {
                    "rappel_id": rappel.id,
                    "advice_timing": "variable",
                    "timing": 0,
                }
            )

    # Comprueba que timing variable = 100 está fuera del rango permitido y lanza ValidationError.
    def test_advice_timing_variable_100_raises(self):
        """Advice con timing variable = 100 lanza ValidationError."""
        rappel = self._make_rappel()
        with self.assertRaises(ValidationError):
            self.env["rappel.advice.email"].create(
                {
                    "rappel_id": rappel.id,
                    "advice_timing": "variable",
                    "timing": 100,
                }
            )

    # Comprueba que timing variable negativo está fuera del rango permitido y lanza ValidationError.
    def test_advice_timing_variable_negative_raises(self):
        """Advice con timing variable negativo lanza ValidationError."""
        rappel = self._make_rappel()
        with self.assertRaises(ValidationError):
            self.env["rappel.advice.email"].create(
                {
                    "rappel_id": rappel.id,
                    "advice_timing": "variable",
                    "timing": -5,
                }
            )


class TestProductNoRappel(TestRappelBase):
    """Tests para el campo no_rappel en producto."""

    # Comprueba que el campo no_rappel de un producto recién creado tiene valor False por defecto.
    def test_product_no_rappel_default_false(self):
        """Por defecto no_rappel es False en el producto."""
        self.assertFalse(self.product.no_rappel)

    # Comprueba que marcar no_rappel=True en el product.template propaga el valor al product.product.
    def test_product_no_rappel_set(self):
        """Se puede marcar no_rappel en el template."""
        self.product.product_tmpl_id.no_rappel = True
        self.assertTrue(self.product.no_rappel)


class TestResPartnerRappel(TestRappelBase):
    """Tests para la relación partner-rappel."""

    # Comprueba que al crear una relación res.partner.rappel.rel, ésta aparece en partner.rappel_ids.
    def test_partner_rappel_ids(self):
        """El partner tiene rappel_ids accesible."""
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel Partner",
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
                "date_start": date.today(),
                "periodicity": "annual",
            }
        )
        self.assertIn(rel, self.partner.rappel_ids)


class TestRappelCalculatedNameGet(TestRappelBase):
    """Tests para RappelCalculated."""

    # Comprueba que display_name de rappel.calculated incluye el nombre del partner en el resultado.
    def test_rappel_calculated_name_get(self):
        """display_name devuelve 'partner start - end'."""
        calc = self.env["rappel.calculated"].create(
            {
                "partner_id": self.partner.id,
                "rappel_id": self.env["rappel"].create(
                    {
                        "name": "Rappel NG",
                        "type_id": self.rappel_type.id,
                        "qty_type": "value",
                        "calc_mode": "fixed",
                        "calc_amount": "percent",
                        "fix_qty": 1.0,
                        "global_application": True,
                    }
                ).id,
                "date_start": date.today(),
                "date_end": date.today(),
                "quantity": 10.0,
            }
        )
        name = calc.display_name
        self.assertIn(self.partner.name, name)


class TestRappelConstraintOnWrite(TestRappelBase):
    """Verifica que la constraint _check_application también aplica en write."""

    # Comprueba que la constraint _check_application se dispara también al modificar (write) un rappel existente.
    def test_check_application_on_write(self):
        """Modificar un rappel para quitar global sin producto lanza ValidationError."""
        rappel = self.env["rappel"].create(
            {
                "name": "Rappel Write Check",
                "type_id": self.rappel_type.id,
                "qty_type": "value",
                "calc_mode": "fixed",
                "calc_amount": "percent",
                "fix_qty": 5.0,
                "global_application": True,
            }
        )
        with self.assertRaises(ValidationError):
            rappel.write({"global_application": False})
