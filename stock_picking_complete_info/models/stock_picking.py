# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons import decimal_precision as dp


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    auto_create_post_process_batch = fields.Boolean('Auto create batch',
                                                    help="Allow create a new batch when transfer a batch")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def _count_product_ids(self):
        for pick in self:
            count = len(pick.move_line_ids.mapped('product_id'))
            pick.product_ids_count = count

    reserved_availability = fields.Float(
        'Quantity Reserved', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    quantity_done = fields.Float(
        'Quantity Done', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    product_uom_qty = fields.Float(
        'Quantity', compute='compute_picking_qties',
        digits=dp.get_precision('Product Unit of Measure'))
    product_ids_count = fields.Integer('# Products',
                                       compute='_count_product_ids')
    all_assigned = fields.Boolean('100% reservado', compute='_compute_state', store=True, copy=False)
    currency_id = fields.Many2one(related='sale_id.currency_id')
    price_subtotal = fields.Monetary(string='Subtotal', currency_field='currency_id', compute='get_n_lines', store=True)
    move_lines_count = fields.Integer('# Lineas', compute='get_n_lines', store=True)
    info_str = fields.Char('Info str', compute='get_n_lines', store=True)
    n_lines = fields.Char(store=False)
    n_amount = fields.Char(store=False)

    @api.multi
    def write(self, vals):
        batch_ids = self.mapped('batch_id')
        if batch_ids and any(x.state =='in_progress' for x in batch_ids):
            raise ValidationError('Estás intentado modificar algún albarán que ya está en una agrupación que se está realizando.\n Para poder hacerlo:\nSaca el albrán de la agrupación o ...\nCambia el estado de la agrupación')
        return super().write(vals)


    @api.depends('move_type', 'move_lines.state', 'move_lines.picking_id')
    @api.one
    def _compute_state(self):

        '''
        TODO SOBREESCRIBO TODO PQ NO HE ENCONTRADO OTRA HERENCIA, SI LA HUBIERA
        super()._compute_state()
        if self.move_lines._get_relevant_state_among_moves() in ('assigned', 'done'):
            self.all_assigned = True
        else:
          self.all_assigned = False
        todo ..................................................................
        '''

        ''' State of a picking depends on the state of its related stock.move
        - Draft: only used for "planned pickings"
        - Waiting: if the picking is not ready to be sent so if
          - (a) no quantity could be reserved at all or if
          - (b) some quantities could be reserved and the shipping policy is "deliver all at once"
        - Waiting another move: if the picking is waiting for another move
        - Ready: if the picking is ready to be sent so if:
          - (a) all quantities are reserved or if
          - (b) some quantities could be reserved and the shipping policy is "as soon as possible"
        - Done: if the picking is done.
        - Cancelled: if the picking is cancelled
        '''
        self.all_assigned = False
        if not self.move_lines:
            self.state = 'draft'
        elif any(move.state == 'draft' for move in self.move_lines):  # TDE FIXME: should be all ?
            self.state = 'draft'
        elif all(move.state == 'cancel' for move in self.move_lines):
            self.state = 'cancel'
        elif all(move.state in ['cancel', 'done'] for move in self.move_lines):
            self.state = 'done'
        else:
            relevant_move_state = self.move_lines._get_relevant_state_among_moves()
            if relevant_move_state in ('assigned', 'done'):
                self.all_assigned = True
            if relevant_move_state == 'partially_available':
                self.state = 'assigned'
            else:
                self.state = relevant_move_state

    @api.multi
    @api.depends('move_lines', 'state')
    def get_n_lines(self):
        for pick in self:
            pick._compute_state()
            pick.price_subtotal = sum(x.price_subtotal for x in pick.move_lines)
            move_id_count= len(pick.move_lines)
            # if pick.picking_type_id.code == 'outgoing':
            #     lines_for_total = pick.move_lines
            # else:
            #     lines_for_total = pick.move_lines.mapped('move_dest_ids').filtered(
            #         lambda x: x.picking_type_id.code == 'outgoing')

            if pick.state == 'done':
                pick.move_lines_count = len(pick.move_lines)
                move_lines_count_not = pick.move_lines_count = len(pick.move_lines)
                state_text = 'Validadas'
            elif pick.state == 'assigned':
                move_lines_count_not = len(pick.move_lines.filtered(lambda x: x.reserved_availability))
                pick.move_lines_count = move_lines_count_not
                state_text = 'Reservadas'
            else:
                pick.move_lines_count = len(pick.move_lines)
                state_text = 'Sin reserva'
                move_lines_count_not = pick.move_lines_count - len(
                    pick.move_lines.filtered(lambda x: x.reserved_availability))
            pick.info_str = _('{} €: {} {} of {} lines'.format(pick.price_subtotal, state_text, move_lines_count_not,
                                                               move_id_count))

    @api.multi
    def unlink_from_batch(self):
        self.write({'batch_id': False})

    @api.multi
    def compute_picking_qties(self):
        for pick in self:
            pick.quantity_done = sum(x.quantity_done for x in pick.move_lines)
            pick.reserved_availability = sum(x.reserved_availability for x in pick.move_lines)
            pick.product_uom_qty = sum(x.product_uom_qty for x in pick.move_lines)

    @api.multi
    def force_set_qty_done(self):
        field = self._context.get('field', 'product_uom_qty')
        reset = self._context.get('reset', True)
        states = ('confirmed', 'assigned')
        for picking in self:
            if picking.state not in states:
                raise ValidationError(_('State {} incorrect for {}'.format(picking.state, picking.name)))
            picking.move_lines.force_set_qty_done(reset, field)

    @api.multi
    def action_view_product_lst(self):
        self.ensure_one()
        products = self.move_line_ids.mapped('product_id')
        action = self.env.ref(
            'product.product_normal_action').read()[0]
        if len(products) > 1:
            action['domain'] = [('id', 'in', products.ids)]
        elif len(products) == 1:
            form_view_name = 'product.product_normal_form_view'
            action['views'] = [
                (self.env.ref(form_view_name).id, 'form')]
            action['res_id'] = products.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self._context.get('n_amount') == True:
            for arg in args:
                if arg[0] == 'n_amount':
                    if '-' in arg[2]:
                        try:
                            min, max = arg[2].split('-')
                            min = ['price_subtotal', '>=', min]
                            max = ['price_subtotal', '<=', max]
                            args += [min]
                            args += [max]
                        except:
                            pass
                    else:
                        try:
                            min = ['price_subtotal', '=', arg[2]]
                            args += [min]
                        except:
                            pass
                    args.remove(arg)
                    break
        if self._context.get('n_lines') == True:
            for arg in args:
                if arg[0] == 'n_lines':
                    if '-' in arg[2]:
                        try:
                            min, max = arg[2].split('-')
                            min = ['move_lines_count', '>=', min]
                            max = ['move_lines_count', '<=', max]
                            args += [min]
                            args += [max]
                        except:
                            pass
                    else:
                        try:
                            min = ['move_lines_count', '=', arg[2]]
                            args += [min]
                        except:
                            pass
                    args.remove(arg)
                    break
        return super().search(args, offset, limit, order, count)