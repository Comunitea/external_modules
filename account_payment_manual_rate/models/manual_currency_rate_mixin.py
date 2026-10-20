# Copyright 2026 Comunitea
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class ManualCurrencyRateMixin(models.AbstractModel):
    """Reusable fields to let the user type an exchange rate by hand.

    As Odoo does for the rate of invoices, the rate is a single editable field
    that defaults to the system rate for the date. It is considered manual
    when it differs from the expected one.

    Rates follow the Odoo convention of ``res.currency.rate``:

    * ``manual_rate``: units of the currency per 1 unit of the base currency.
    * ``manual_inverse_rate``: units of the base currency per 1 unit of the
      currency.

    Models using the mixin must override ``_compute_manual_rate_context`` to
    tell which company, base currency, currency and date the rate refers to.
    For payments the base currency is the company currency.
    """

    _name = "manual.currency.rate.mixin"
    _description = "Manual Currency Rate Mixin"

    manual_rate_company_id = fields.Many2one(
        comodel_name="res.company", compute="_compute_manual_rate_context"
    )
    manual_rate_base_currency_id = fields.Many2one(
        comodel_name="res.currency", compute="_compute_manual_rate_context"
    )
    manual_rate_currency_id = fields.Many2one(
        comodel_name="res.currency", compute="_compute_manual_rate_context"
    )
    manual_rate_date = fields.Date(compute="_compute_manual_rate_context")
    manual_rate_available = fields.Boolean(
        compute="_compute_manual_rate_available",
        help="The currency differs from the base one, so a rate is meaningful.",
    )
    manual_rate_expected = fields.Float(
        compute="_compute_manual_rate_expected", digits=0
    )
    use_manual_rate = fields.Boolean(
        string="Manual Exchange Rate",
        compute="_compute_use_manual_rate",
        help="The exchange rate differs from the one defined in the system.",
    )
    manual_rate = fields.Float(
        string="Exchange Rate",
        compute="_compute_manual_rate",
        store=True,
        readonly=False,
        copy=False,
        digits=0,
        help="Units of the currency per 1 unit of the base currency.",
    )
    manual_inverse_rate = fields.Float(
        string="Inverse Exchange Rate",
        compute="_compute_manual_inverse_rate",
        store=True,
        readonly=False,
        copy=False,
        digits=0,
        help="Units of the base currency per 1 unit of the currency.",
    )

    def _compute_manual_rate_context(self):
        raise NotImplementedError(
            "Models using manual.currency.rate.mixin must define the company, "
            "currency and date of the rate."
        )

    @api.depends("manual_rate_base_currency_id", "manual_rate_currency_id")
    def _compute_manual_rate_available(self):
        for record in self:
            record.manual_rate_available = bool(
                record.manual_rate_base_currency_id
                and record.manual_rate_currency_id
                and record.manual_rate_currency_id
                != record.manual_rate_base_currency_id
            )

    @api.depends(
        "manual_rate_company_id",
        "manual_rate_base_currency_id",
        "manual_rate_currency_id",
        "manual_rate_date",
    )
    def _compute_manual_rate_expected(self):
        for record in self:
            record.manual_rate_expected = record._get_system_manual_rate()

    @api.depends("manual_rate", "manual_rate_expected", "manual_rate_available")
    def _compute_use_manual_rate(self):
        for record in self:
            record.use_manual_rate = bool(
                record.manual_rate_available
                and float_compare(
                    record.manual_rate, record.manual_rate_expected, precision_digits=9
                )
            )

    @api.depends(
        "manual_rate_company_id",
        "manual_rate_base_currency_id",
        "manual_rate_currency_id",
        "manual_rate_date",
    )
    def _compute_manual_rate(self):
        for record in self:
            record.manual_rate = record._get_system_manual_rate()

    @api.depends("manual_rate")
    def _compute_manual_inverse_rate(self):
        for record in self:
            record.manual_inverse_rate = (
                1.0 / record.manual_rate if record.manual_rate else 0.0
            )

    @api.onchange("manual_inverse_rate")
    def _onchange_manual_inverse_rate(self):
        for record in self:
            if record.manual_inverse_rate:
                record.manual_rate = 1.0 / record.manual_inverse_rate

    @api.constrains("manual_rate")
    def _check_manual_rate(self):
        for record in self:
            if record.manual_rate_available and record.manual_rate <= 0:
                raise ValidationError(
                    self.env._("The exchange rate must be strictly positive.")
                )

    def _get_system_manual_rate(self):
        """Rate (currency units per base currency unit) defined in the system."""
        self.ensure_one()
        company = self.manual_rate_company_id
        base = self.manual_rate_base_currency_id
        currency = self.manual_rate_currency_id
        if not company or not base or not currency or currency == base:
            return 1.0
        return base._get_conversion_rate(
            base,
            currency,
            company,
            self.manual_rate_date or fields.Date.context_today(self),
        )

    def _manual_rate_applies(self):
        self.ensure_one()
        return bool(
            self.manual_rate_available
            and self.use_manual_rate
            and self.manual_rate > 0
        )

    def _manual_rate_convert(self, amount):
        """Convert ``amount`` from the currency to the base currency."""
        self.ensure_one()
        return self.manual_rate_base_currency_id.round(amount / self.manual_rate)

    def action_refresh_manual_rate(self):
        """Reset the rate to the one defined in the system."""
        for record in self:
            record.manual_rate = record._get_system_manual_rate()

    def _manual_rate_vals(self):
        self.ensure_one()
        return {
            "manual_rate": self.manual_rate,
            "manual_inverse_rate": self.manual_inverse_rate,
        }

    @api.model
    def _manual_rate_normalize_vals(self, vals):
        # The rate is the source of truth: derive it when only the inverse is given.
        if vals.get("manual_inverse_rate") and "manual_rate" not in vals:
            vals["manual_rate"] = 1.0 / vals["manual_inverse_rate"]
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._manual_rate_normalize_vals(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._manual_rate_normalize_vals(vals)
        return super().write(vals)
