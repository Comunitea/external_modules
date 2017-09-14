# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from odoo import models, fields


class AcountBankingMandates(models.Model):

    _inherit = "account.banking.mandate"
    _order = "by_default desc, partner_bank_id desc"

    active = fields.\
        Boolean("Active", related="partner_bank_id.active", readonly=True,
                help="This field depends on bank account field value")
    by_default = fields.Boolean("By default")
