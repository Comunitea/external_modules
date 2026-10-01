from odoo import fields
from odoo.tests.common import TransactionCase


class TestResCurrencyRateForce(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.currency_from, cls.currency_to = cls.env["res.currency"].create(
            [
                {"name": "FOR", "symbol": "FOR"},
                {"name": "TOO", "symbol": "TOO"},
            ]
        )
        cls.test_date = fields.Date.to_date("2020-01-01")
        cls.env["res.currency.rate"].create(
            [
                {
                    "name": cls.test_date,
                    "rate": 2.0,
                    "currency_id": cls.currency_from.id,
                    "company_id": cls.company.id,
                },
                {
                    "name": cls.test_date,
                    "rate": 4.0,
                    "currency_id": cls.currency_to.id,
                    "company_id": cls.company.id,
                },
            ]
        )

    def test_without_forced_rate_uses_standard_conversion(self):
        rate = self.currency_from._get_conversion_rate(
            self.currency_from,
            self.currency_to,
            self.company,
            self.test_date,
        )

        self.assertEqual(rate, 2.0)

    def test_forced_from_rate(self):
        rate = self.currency_from.with_context(
            force_from_rate=8.0
        )._get_conversion_rate(
            self.currency_from,
            self.currency_to,
            self.company,
            self.test_date,
        )

        self.assertEqual(rate, 0.5)

    def test_forced_to_rate(self):
        rate = self.currency_from.with_context(
            force_to_rate=10.0
        )._get_conversion_rate(
            self.currency_from,
            self.currency_to,
            self.company,
            self.test_date,
        )

        self.assertEqual(rate, 5.0)

    def test_forced_from_and_to_rates(self):
        rate = self.currency_from.with_context(
            force_from_rate=8.0,
            force_to_rate=10.0,
        )._get_conversion_rate(
            self.currency_from,
            self.currency_to,
            self.company,
            self.test_date,
        )

        self.assertEqual(rate, 1.25)

    def test_forced_rate_is_used_by_convert(self):
        converted = self.currency_from.with_context(
            force_from_rate=8.0
        )._convert(
            100.0,
            self.currency_to,
            self.company,
            self.test_date,
            round=False,
        )

        self.assertEqual(converted, 50.0)

    def test_same_currency_returns_one(self):
        rate = self.currency_from.with_context(
            force_from_rate=8.0,
            force_to_rate=10.0,
        )._get_conversion_rate(
            self.currency_from,
            self.currency_from,
            self.company,
            self.test_date,
        )

        self.assertEqual(rate, 1.0)
