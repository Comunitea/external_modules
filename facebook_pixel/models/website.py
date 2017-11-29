# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class Website(models.Model):

    _inherit = 'website'

    pixel_id = fields.Char('Facebok pixel id')

    pixel_script = fields.Char(compute='_compute_pixel_script', store=True)

    @api.depends('pixel_id')
    def _compute_pixel_script(self):
        self.pixel_script = """!function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '%s');
            fbq('track', 'PageView');""" % self.pixel_id


class WebsiteConfig(models.Model):

    _inherit = 'website.config.settings'


    pixel_id = fields.Char('Facebok pixel id',
                                   related='website_id.pixel_id')
