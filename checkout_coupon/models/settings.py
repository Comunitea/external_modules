# -*- coding: utf-8 -*-
# © 2018 Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class Website(models.Model):
    _inherit = 'website'

    use_osc_coupon = fields.Boolean('Coupon module is active', default=False)


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'
    _name = 'checkout_coupon.settings'

    def _default_website(self):
        return self.env['website'].search([], limit=1)

    website_id = fields.Many2one('website', string="website", default=_default_website, required=True)
    use_osc_coupon = fields.Boolean('Coupon module is active', related='website_id.use_osc_coupon')

    def activate_coupons(self):
        for r in self:
            r.write({'use_osc_coupon': True})

    def deactivate_coupons(self):
        for r in self:
            r.write({'use_osc_coupon': False})
