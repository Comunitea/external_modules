from odoo import api, models


class ResCurrency(models.Model):

    _inherit = "res.currency"

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency):
        from_currency = from_currency.with_env(self.env)
        to_currency = to_currency.with_env(self.env)
        to_rate = to_currency.rate
        from_rate = from_currency.rate
        if self._context.get('force_from_rate'):
            from_rate = self._context['force_from_rate']
        if self._context.get('force_to_rate'):
            to_rate = self._context['force_to_rate']
        return to_rate / from_rate
