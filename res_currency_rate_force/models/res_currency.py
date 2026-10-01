from odoo import api, fields, models


class ResCurrency(models.Model):

    _inherit = "res.currency"

    @api.model
    def _get_conversion_rate(
        self, from_currency, to_currency, company=None, date=None
    ):
        if from_currency == to_currency:
            return 1.0

        forced_from_rate = self.env.context.get("force_from_rate")
        forced_to_rate = self.env.context.get("force_to_rate")
        if forced_from_rate is None and forced_to_rate is None:
            return super()._get_conversion_rate(
                from_currency, to_currency, company, date
            )

        company = company or self.env.company
        if company == self.env.company.root_id:
            company = self.env.company
        date = date or fields.Date.context_today(self)

        from_currency = from_currency.with_company(company).with_context(
            date=str(date)
        )
        to_currency = to_currency.with_company(company).with_context(date=str(date))
        from_rate = from_currency.rate
        to_rate = to_currency.rate

        if forced_from_rate is not None:
            from_rate = forced_from_rate
        if forced_to_rate is not None:
            to_rate = forced_to_rate

        return to_rate / from_rate
