# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockQuantPackage(models.Model):

    _inherit = "stock.quant.package"

    quant_quantity = fields.Float(
        'Quantity',
        help='Quantity in this package, in the default unit of measure of the product',
        compute='get_product_quant_quantity')
    available_quant_quantity = fields.Float(
        'Available Quantity',
        default=0.0,
        help='Not reserved quantity in this package, in the default unit of measure of the product',
        compute='get_product_quant_quantity')

    product_id = fields.Many2one('product.product', compute='get_package_unique_values', store=True)
    uom_id = fields.Many2one('product.uom', compute='get_package_unique_values', store=True)
    lot_id = fields.Many2one('stock.production.lot', compute='get_package_unique_values', store=True)
    mono_product = fields.Boolean('Mono product', compute='get_package_unique_values', store=True)

    @api.depends('quant_ids')
    def get_package_unique_values(self):
        for package in self:
            if package and package.quant_ids:
                _sql = "select " \
                       "CASE WHEN count(*) = 1 THEN sq.product_id ELSE 0 END as product_id, " \
                       "CASE WHEN count(*) = 1 THEN sq.lot_id ELSE 0 END as lot_id, " \
                       "pt.uom_id "
                _from = "from stock_quant sq " \
                        "join product_product pp on pp.id = sq.product_id " \
                        "join product_template pt on pp.product_tmpl_id = pt.id " \
                        "where sq.package_id = {} ".format(package.id)

                if self.env.user.id != 1:
                    _from = "{} and sq.company_id = {} ".format(_from, self.env.user.company_id)

                _group = "group by sq.product_id, sq.lot_id, sq.location_id, pt.uom_id"
                sql = "{}{}{}".format(_sql, _from, _group)
                self.env.cr.execute(sql)
                res = self.env.cr.fetchall()
                res = res and res[0] or (False, False, False)
                package.product_id = res[0]
                package.lot_id = res[1]
                package.uom_id = res[2]
                package.mono_product = True if res[0] else False

    @api.multi
    def get_product_quant_quantity(self, location_id=False, lot_id=None, package_id=None, owner_id=None):
        quant_obj = self.env['stock.quant']
        location_id = self.env['stock.location'].browse(location_id) or self.location_id
        for package in self:
            if not package.product_id:
                package.quant_quantity= 0.00
                package.available_quant_quantity = 0.00
                continue
            quants = quant_obj._gather(package.product_id, location_id=location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=False)
            package.quant_quantity = sum(quants.mapped('quantity'))
            package.available_quant_quantity = package.quant_quantity - sum(quants.mapped('reserved_quantity'))

    @api.model
    def _get_same_alternative_packages(self, product_id= False, location_id=False, lot_id=False, package_id=False, owner_id=False, domain=[]):
        ## devuelve una lista con quants agrupados disponibles para seleección
        if not location_id:
            return []
        product_id = product_id and self.env['product.product'].browse(product_id) or self.product_id
        if not product_id:
            return False
        location_id = self.env['stock.location'].browse(location_id)
        quants = self.env['stock.quant']._gather(self.product_id,
                                                 location_id=location_id.parent_view_location_id,
                                                 lot_id=lot_id,
                                                 package_id=package_id or self,
                                                 owner_id=owner_id,
                                                 strict=self.product_id.tracking != 'none')

        quants_available = quants.filtered(lambda x: x.location_id in location_id.parent_view_location_id.child_ids and (x.quantity - x.reserved_quantity) > 0)

        return [(q.lot_id, q.name, q.ref, q.product_id, q.available_qty, q.location_id) for q in quants_available]


    @api.model
    def get_apk_vals(self, type='normal'):
        if not self:
            return False
        vals = {'id': self.id,
                'name': self.name}

        if type != 'min':
            vals.update({'quant_quantity': self.quant_quantity,
                         'available_quant_quantity': self.available_quant_quantity,
                         'location_id': self.location_id.get_apk_vals('min'),
                         'product_id': self.product_id.get_apk_vals('min'),
                         })
        print('Paquete: valores {} \n {}'.format(type, vals))
        return vals

