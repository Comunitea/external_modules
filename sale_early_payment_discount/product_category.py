# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""Add a new property for early payment discount account by default"""

from openerp.osv import osv, fields

class product_category(osv.osv):
    """Add a new property for early payment discount account by default"""
    _inherit = 'product.category'

    _columns = {
        'property_account_sale_early_payment_disc': fields.property('account.account',
            type='many2one', relation='account.account',
            string='Sale early payment account', method=True, view_load=True,
            help='This account will be used to input the early payments discount in sale')
    }