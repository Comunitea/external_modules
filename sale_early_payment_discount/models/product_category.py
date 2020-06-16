# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class ProductCategory(models.Model):

    _inherit = 'product.category'

    property_account_sale_early_payment_disc = fields.Many2one(
        'account.account', 'Sale early payment account',
        help='This account will be used to input the early payments discount \
             in sale', company_dependent=True)


class ProductTemplate(models.Model):

    _inherit = "product.template"

    without_early_payment = fields.Boolean("Without early payment")
