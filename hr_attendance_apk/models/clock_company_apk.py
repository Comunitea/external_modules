# Copyright 2019 Comunitea Servicios Tecnológicos S.L.

from odoo import api, models, fields, tools, _

MIN_MINUTE = 0


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def get_clock_apk(self):
        apk = self.env['clock.company.apk'].\
            search([('company_id', '=', self.id)], limit=1)
        return apk

    @api.multi
    def action_view_clock_company_apk_form(self):
        self.ensure_one()

        action = {
            'type': 'ir.actions.act_window',
            'name': _('Info Apk'),
            'res_model': 'clock.company.apk',
            'domain': "[('id', '=', %s)]" % self.id,
            'auto_search': True,
            'views': [
                (self.env.ref('hr_attendance_apk.view_clock_company_apk_form').id, 'form')],
            'target': 'current',
            'nodestroy': True,
        }

        return action


class ClockCompanyApk(models.Model):
    _name = "clock.company.apk"

    @api.multi
    def _get_image(self):
        for p in self:
            p.image_medium = tools.\
                image_get_resized_images(p.image)['image_medium']
            p.image_small = tools.\
                image_get_resized_images(p.image)['image_small']

    company_id = fields.Many2one('res.company')
    name = fields.Char()
    image = fields.Binary('Image', help='Logo in apk', attachment=True)
    image_medium = fields.Binary('Image medium', compute='_get_image')
    image_small = fields.Binary('Image medium', store=False,
                                compute='_get_image')

    welcome_message = fields.Char("Welcome message")
    logo_color = fields.Char("Logo color")
    contact_phone = fields.Char("Contact phone")
    min_minute = fields.Integer('Minutes between logs', default=3)
    min_accuracity = fields.Integer('Min. accuraccity', default=100)
    distance_filter = fields.\
        Integer('Min. Distance', default=500,
                help="The minimum distance (measured in meters) a device must "
                     "move horizontally before an update event is generated.")
    stationary_radius = fields.\
        Integer('Stationary radius', default=50,
                help="When stopped, the minimum distance the device must move "
                     "beyond the stationary location for aggressive "
                     "background-tracking to engage.")

    @api.model
    def get_company_apk_config(self, vals):
        company_id = vals.get('company_id', False)
        apk_config = self.env['clock.company.apk'].\
            search([('company_id', '=', company_id)], limit=1)

        values = {
            'interval': apk_config.min_minute*60,
            'min_accuracity': apk_config.min_accuracity,
            'distance_filter': apk_config.distance_filter,
            'stationary_radius': apk_config.stationary_radius
        }

        return values
