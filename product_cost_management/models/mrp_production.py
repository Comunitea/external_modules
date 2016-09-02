# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos (<http://www.comunitea.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, SUPERUSER_ID


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_production_end(self, cr, uid, ids, context=None):
        t_move = self.pool.get('stock.move')
        t_quant = self.pool.get('stock.quant')
        for production in self.browse(cr, uid, ids, context=context):
            move_ids = [x.id for x in production.move_created_ids2]
            t_move.get_price_from_cost_structure(cr, uid, move_ids, context)
            for move in production.move_created_ids2:
                quant_ids = [x.id for x in move.quant_ids]
                t_quant.write(cr, SUPERUSER_ID, quant_ids,
                              {'cost': move.price_unit}, context=context)
                move.update_product_price()  # Update price in product.template
        res = super(MrpProduction, self).action_production_end(cr, uid, ids,
                                                          context=context)
        return res
