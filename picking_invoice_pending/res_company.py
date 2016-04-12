# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Omar Castiñeira Saavedra <omar@comunitea.com>$
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

from openerp import models, fields


class ResCompany(models.Model):

    _inherit = "res.company"

    property_pending_supplier_invoice_account = \
        fields.Many2one("account.account", "Pending supplier invoice account",
                        domain=[('type', '=', 'payable')],
                        help="This account is used for accounting in pending "
                             "supplier invoices.", company_dependent=True)
    property_pending_stock_journal = \
        fields.Many2one("account.journal", "Pending supplier invoice journal",
                        help="This journal is used for accounting in pending "
                             "supplier invoices.", company_dependent=True)
    required_invoice_pending_move = fields.Boolean('Require pending move',
                                                   help="Require pending move "
                                                        "to done incoming "
                                                        "picking")
