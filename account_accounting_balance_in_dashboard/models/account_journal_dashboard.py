##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2025 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See thefire
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    show_accounting_balance_dashboard = fields.Boolean(
        string="Show Accounting Balance in Dashboard",
        default=False
    )

    def _fill_bank_cash_dashboard_data(self, dashboard_data):
        res = super()._fill_bank_cash_dashboard_data(dashboard_data)
        for journal in self.filtered(lambda x: x.show_accounting_balance_dashboard):
            if journal.id in dashboard_data:
                dashboard_data[journal.id].update({
                    'accounting_balance': journal.default_account_id.current_balance,
                    'show_accounting_balance': True if journal.show_accounting_balance_dashboard else False,
                })
        return res
