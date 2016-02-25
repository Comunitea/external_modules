# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013
#    Pexego Sistemas Informáticos (http://www.pexego.es)
#    Copyright (C) 2015
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
#    $Omar Castiñeira Saavedra$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class account_balance_full_report(models.TransientModel):

    _inherit = "trial.balance.webkit"

    business_line_ids = fields.\
        Many2many('account.business.line',
                  'trial_balance_report_account_business_line_rel',
                  'wizard_id', 'business_line_id', 'Business lines')

    @api.multi
    def _print_report(self, data):
        res = super(account_balance_full_report, self)._print_report(data)
        if self[0].business_line_ids:
            res['datas']["form"]["used_context"]["business_lines"] =\
                [x.id for x in self[0].business_line_ids]

        return res
