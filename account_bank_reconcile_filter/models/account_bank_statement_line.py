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

from openerp import models, api, fields


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    @api.model
    def _domain_move_lines_for_reconciliation(
            self, st_line, excluded_ids=None, str=False,
            additional_domain=None):
        domain = super(AccountBankStatementLine, self)\
            ._domain_move_lines_for_reconciliation(
                st_line, excluded_ids=excluded_ids, str=str,
                additional_domain=additional_domain)
        if str:
            domain.insert(-1, '|', )
            domain.append ('|', )
            domain.append(('account_id.name', 'ilike', str))
            domain.append(('account_id.code', 'ilike', str))
        return domain