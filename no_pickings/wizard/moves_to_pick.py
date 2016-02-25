# -*- coding: utf-8 -*-

from openerp import models, _, api, exceptions, fields


class MovesToPick(models.TransientModel):

    _name = "moves.to.pick"

    name = fields.Char("Name")

    @api.model
    def view_init(self, fields_list):
        res = super(MovesToPick, self).view_init(fields_list)
        id_address = False
        id_warehouse = False
        move_ids = self.env.context.get('active_ids', [])

        if not move_ids or not \
                self.env.context.get('active_model') == 'stock.move':
            return res

        # Lanzamos una excepción si alguna dirección es diferente
        for m in self.env['stock.move'].browse(move_ids):
            if not id_address:
                id_address = m.partner_id.id
            if not id_warehouse:
                id_warehouse = m.warehouse_id.id
            if m.partner_id.id != id_address:
                raise exceptions.\
                    Warning(_('Customer of moves must be the same.'))
            if m.warehouse_id.id != id_warehouse:
                raise exceptions.\
                    Warning(_('Warehouse of moves must be the same.'))

        return res

    @api.multi
    def to_pick(self):
        if self.env.context.get('active_ids', []):
            move_ids = self.env.context['active_ids']
            # creamos la cabecera del albarán
            moves = self.env["stock.move"].browse(move_ids)
            origins = [x.procurement_id.sale_line_id.order_id.name for x in
                       moves]
            origins = list(set(origins))
            values = {
                'partner_id': moves[0].partner_id.id,
                'invoice_state': '2binvoiced',
                'picking_type_id': moves[0].picking_type_id.id,
                'origin': u",".join(origins),
                'move_lines': [(6, 0, [x.id for x in moves])]
            }
            picking = self.env['stock.picking'].create(values)
            picking.action_confirm()
            action = self.env.ref('stock.action_picking_tree_all')
            result = action.read()[0]
            view = self.env.ref('stock.view_picking_form')
            result['views'] = [(view.id, 'form')]
            result['res_id'] = picking.id
            return result
