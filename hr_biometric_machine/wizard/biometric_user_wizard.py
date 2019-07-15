# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class BiometricUser(models.TransientModel):
    _name = 'biometric.user.wizard'

    @api.model
    def default_get(self, fields):
        res = super(BiometricUser, self).default_get(fields)
        devices = self.env['biometric.machine'].search([])
        if devices:
            res.update(biometric_device=devices[0].id)
        return res

    biometric_device = fields.Many2one(
        'biometric.machine', 'Biometric device',
    )

    @api.multi
    def import_users(self):
        """
        wrapper function
        """
        self.ensure_one()
        self.create_users_in_openerp()

    @api.model
    def create_users_in_openerp(self):
        self.biometric_device.create_user()
