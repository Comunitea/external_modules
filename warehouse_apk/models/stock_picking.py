# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2019 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
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

from odoo import _, api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class StockPicking(models.Model):

    _inherit = 'stock.picking'

    app_integrated = fields.Boolean(related='picking_type_id.app_integrated', store=True)
    picking_fields = fields.Char(related='picking_type_id.picking_fields', store=True)
    move_fields = fields.Char(related='picking_type_id.move_fields', store=True)
    move_line_fields = fields.Char(related='picking_type_id.move_line_fields', store=True)

    @api.model
    def action_assign_pick(self, vals):
        picking = self.browse(vals.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán"}
        res = picking.action_assign()
        return res

    @api.model
    def button_validate_pick(self, vals):
        picking_id = self.browse(vals.get('id', False))
        if not picking_id:
            return {'err': True, 'error': "No se ha encontrado el albarán"}

        ctx = picking_id._context.copy()
        ctx.update(skip_overprocessed_check=True)
        res = picking_id.with_context(ctx).button_validate()
        try:
            if res:
                if res['res_model'] == 'stock.immediate.transfer':
                    wiz =  self.env['stock.immediate.transfer'].with_context(res['context']).browse(res['res_id'])
                    res_inm = wiz.process()

                    if res_inm['res_model'] == 'stock.backorder.confirmation':
                        wiz = self.env['stock.backorder.confirmation'].with_context(res_inm['context']).browse(res_inm['res_id'])
                        res_bord = wiz._process()

                if res['res_model'] == 'stock.backorder.confirmation':
                        wiz = self.env['stock.backorder.confirmation'].with_context(res['context']).browse(res['res_id'])
                        res_boc = wiz._process()
            return {'err': False, 'values': {'id': picking_id.id, 'state': picking_id.state}}
        except Exception as e:
            return {'err': e}


    @api.model
    def force_set_qty_done_apk(self, vals):
        picking = self.browse(vals.get('id', False))
        field = vals.get('field', False)
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán."}

        ctx = self._context.copy()
        ctx.update(model_dest="stock.move.line")
        ctx.update(field=field)
        res = picking.with_context(ctx).force_set_qty_done()            
        return True

    @api.model
    def force_reset_qties_apk(self, vals):
        picking = self.browse(vals.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán."}
        ctx = self._context.copy()
        ctx.update(reset=True)
        res = picking.with_context(ctx).force_set_qty_done() 
        return True