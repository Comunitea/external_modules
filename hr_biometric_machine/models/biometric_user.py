# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, models


class BiometricUser(models.Model):
    _name = 'biometric.user'

    biometric_id = fields.Integer('Id in biometric device')
    name = fields.Char('Name in biometric device')
    employee_id = fields.Many2one('hr.employee', 'Related employee')
    biometric_device = fields.Many2one(
        'biometric.machine', 'Biometric device',
    )

    _sql_constraints = [
        ('employee_id_uniq', 'unique (employee_id)',
         'It is not possible relate an employee with a biometric user '
         'more than once!'),
    ]

    _sql_constraints = [
        ('biometric_id_uniq', 'unique (biometric_id)',
         'It is not possible to crate more than one '
         'with the same biometric_id'),
    ]
