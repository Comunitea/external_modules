# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    no_promo = fields.Boolean('No Apply promotions',
                              help='If checked the product will be ignored \
                              when apply promotions')


class ProductPackaging(models.Model):

    _inherit = 'product.packaging'

    ul_type = fields.Selection([('unit', 'Unit'), ('pack', 'Pack'),
                                ('box', 'Box'), ('pallet', 'Pallet')],
                               'Logitic Unit Type')
