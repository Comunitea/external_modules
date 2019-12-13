# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons import decimal_precision as dp

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    auto_create_post_process_batch = fields.Boolean('Auto create batch', help="Allow create a new batch when transfer a batch")

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
    all_assigned = fields.Boolean('All assigned', compute='get_all_assigned')
    currency_id = fields.Many2one(related='sale_id.currency_id')
    price_subtotal = fields.Monetary(string='Subtotal', currency_field='currency_id', compute='get_n_lines',store=True)
    move_lines_count = fields.Integer ('# Lines', compute='get_n_lines',store=True)
    info_str = fields.Char('Info str', compute='get_n_lines',store=True)
    n_lines = fields.Char(store=False)
    n_amount = fields.Char(store=False)

    @api.multi
    @api.depends('move_lines', 'state')
    def get_n_lines(self):
        for pick in self:
            if pick.state == 'done':
                move_lines_count_not = pick.move_lines_count = len(pick.move_lines)
                pick.price_subtotal = sum(x.price_subtotal for x in pick.move_lines.filtered(
                    lambda x: x.state == 'done'))
                state_text = 'Done'
            elif pick.state == 'assigned':
                pick.move_lines_count = len(pick.move_lines)
                move_lines_count_not = len(pick.move_lines.filtered(lambda x: x.reserved_availability))
                pick.price_subtotal = sum(x.price_subtotal for x in pick.move_lines.filtered(
                    lambda x: x.state in ('partially_available', 'assigned')))
                state_text = 'Assigned'
            else:
                state_text = 'To assign'
                pick.price_subtotal = sum(x.price_subtotal for x in pick.move_lines.filtered(
                    lambda x: x.state not in ('draft', 'cancel')))
                move_lines_count_not = pick.move_lines_count = len(pick.move_lines)
            pick.info_str = _('{} €: {} {} of {} lines'.format(pick.price_subtotal, state_text, move_lines_count_not, pick.move_lines_count))

    @api.multi
    def get_all_assigned(self):
        for pick in self:
            pick.all_assigned = not any(x.state in ('partially_available', 'confirmed') for x in pick.move_lines)

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
                raise ValidationError (_('State {} incorrect for {}'.format(picking.state, picking.name)))
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
        print (args)
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

        return super().search(args, offset, limit, order, count)
