# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.osv import expression

class StockProductionLot(models.Model):

    _inherit = "stock.production.lot"


    @api.model
    def get_alternative_lots(self, vals):

        move_id = self.env['stock.move.line'].browse(vals.get('move_id', False))
        location_id = move_id.location_id
        product_qty = move_id.product_uom_qty
        product_id = move_id.product_id

        return self._get_pda_lots(product_id, location_id, product_qty=product_qty)

    @api.model
    def _get_pda_lots(self, product_id=False, location_id=False, lot_id=False, package_id=False, owner_id=False, product_qty=0.00, domain=[]):
        quants = self.env['stock.quant']._gather(product_id=product_id,
                                                 location_id=location_id.parent_view_location_id,
                                                 lot_id = lot_id,
                                                 package_id=package_id,
                                                 owner_id=owner_id,
                                                 strict=False)

        quants_available = quants.filtered(lambda x: x.location_id in location_id.parent_view_location_id.child_ids and (x.quantity - x.reserved_quantity) > product_qty)
        res ={'lots': [{'lot_id': q.lot_id.get_apk_vals('min'),
                       'product_id': q.product_id.get_apk_vals('min'),
                       'uom_id': q.product_uom_id.get_apk_vals('min'),
                       'qty_available': q.quantity - q.reserved_quantity,
                       'package_id': q.package_id.get_apk_vals('min'),
                       'location_id': q.location_id.get_apk_vals('min')}
                     for q in quants_available]}
        return res


    @api.model
    def get_apk_vals(self, type='normal'):
        if not self:
            return False
        vals = {'id': self.id,
                'name': self.name}
        if type!='normal':
            vals.update({'use_date': self.use_date,
                         'ref': self.ref,
                         })
        print('Lote: valores {} \n {}'.format(type, vals))
        return vals