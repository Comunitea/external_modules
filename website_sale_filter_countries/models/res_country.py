# -*- coding: utf-8 -*-
#
# © 2016 Comunitea
# © 2019 Comunitea Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCountry(models.Model):
    _inherit = 'res.country'

    website_available = fields.Boolean(default=False)

    def get_website_sale_states(self, mode='billing'):
        """
        Show only states available for selected country in OSC checkout address form
        """
        res = super(ResCountry, self).get_website_sale_states(mode=mode)
        states = self.env['res.country.state']

        if mode == 'shipping':
            dom = [('country_ids', 'in', self.id), ('website_published', '=', True)]
            delivery_carriers = self.env['delivery.carrier'].sudo().search(dom)

            for carrier in delivery_carriers:
                if not carrier.country_ids and not carrier.state_ids:
                    states = res
                    break
                states |= carrier.state_ids
            if not states:
                states = states.search([('country_id', '=', self.id), ('website_available', '=', True)])
            res = states
        return res


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    website_available = fields.Boolean(default=False)
