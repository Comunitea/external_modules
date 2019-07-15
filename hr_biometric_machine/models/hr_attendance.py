# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    @api.one
    def fix_register(self):
        self.write({'state': 'right'})

    state = fields.Selection(
        selection=[('fix', 'Fix'), ('right', 'Right')],
        default='right',
        help='The user did not register an input '
        'or an output in the correct order, '
        'then the system proposed one or more regiters to fix the problem '
        'but you must review the created register due '
        'becouse of hour could be not correct' )
