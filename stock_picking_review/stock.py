# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
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
from openerp import models, fields, api
from openerp.addons.decimal_precision import decimal_precision as dp
from openerp.tools.translate import _
from openerp.exceptions import except_orm
from openerp.tools.float_utils import float_is_zero
import time
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):

    _inherit = "stock.move"

    accepted_qty = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
        string='Accepted qty (UoS)', copy=False)
    product_uom_acc_qty = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
        string='Accepted qty', copy=False)
    rejected = fields.Boolean('Rejected')

    price_subtotal_accepted = fields.Float(
        compute='_get_subtotal_accepted', string="Subtotal Accepted",
        digits=dp.get_precision('Account'), readonly=True,
        store=False)
    cost_subtotal_accepted = fields.Float(
        compute='_get_subtotal_accepted', string="Cost subtotal Accepted",
        digits=dp.get_precision('Account'), readonly=True,
        store=False)
    margin_accepted = fields.Float(
        compute='_get_subtotal_accepted', string="Margin Accepted",
        digits=dp.get_precision('Account'), readonly=True,
        store=False)
    percent_margin_accepted = fields.Float(
        compute='_get_subtotal_accepted', string="% margin Accepted",
        digits=dp.get_precision('Account'), readonly=True,
        store=False)
    change_price = fields.Boolean("Cambio precio")
    new_price_unit = fields.Float("Nuevo precio (Udm)")
    new_discount = fields.Float("Nuevo descuento")

    @api.multi
    def _check_qty(self):
        res = True
        for move in self:
            if move.accepted_qty > move.product_uos_qty or \
                    move.product_uom_acc_qty > move.product_uom_qty:
                return False
        return res

    _constraints = [
        (_check_qty,
         'Some accepted qty is grater than the original quantity.',
         ['accepted_qty', 'product_uom_acc_qty'])
    ]

    @api.onchange('accepted_qty')
    def accepted_qty_onchange(self):
        """
        We change the product_uom_acc_qty
        """
        product = self.product_id
        t_uom = self.env['product.uom']
        if product:
            qty = self.accepted_qty
            uos_id = self.product_uos.id
            uom_id = self.product_id.uom_id.id
            self.product_uom_acc_qty = t_uom._compute_qty(uos_id, qty, uom_id)

    @api.onchange('product_uom_acc_qty')
    def uom_acc_qty(self):
        """
        We change the accepted_qty
        """
        product = self.product_id
        t_uom = self.env['product.uom']
        if product:
            qty = self.product_uom_acc_qty
            uos_id = self.product_uos.id
            uom_id = self.product_id.uom_id.id
            self.accepted_qty = t_uom._compute_qty(uom_id, qty, uos_id)

    @api.multi
    def _get_subtotal_accepted(self):
        qty = 0
        price = 0
        for move in self:
            _logger.debug("CMNT Calculo en  _get_subtotal_accepted (move)")
            if move.procurement_id.sale_line_id:
                price_unit = move.procurement_id.sale_line_id.price_unit
                price_disc_unit = price_unit
                price = price_disc_unit
                qty = move.product_uom_acc_qty
                sale_line = move.procurement_id.sale_line_id
                taxes = \
                    sale_line.tax_id.compute_all(price, qty,
                                                 move.product_id,
                                                 move.picking_id.partner_id)
                cur = sale_line.order_id.pricelist_id.currency_id
                move.price_subtotal_accepted = cur.round(taxes['total'])

    @api.multi
    def action_done(self):
        res = super(StockMove, self).action_done()
        for move in self:
            if move.picking_id.picking_type_code == 'outgoing':
                move.write({'accepted_qty': move.product_uos_qty,
                            'product_uom_acc_qty': move.product_uom_qty})
        return res

    def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type,
                               context=None):
        res = super(StockMove, self)._get_invoice_line_vals(cr, uid, move,
                                                            partner, inv_type,
                                                            context=context)
        if move.picking_id.state == 'done' and move.picking_id.reviewed:
            # Solo se cogen las cantidades aceptadas para
            # albaranes  finalizados y revisados. Con esto nos aseguramios
            # el comportamiento normal en caso de no pasar por l proceso de
            # devolución
            if move.product_uos and move.accepted_qty:
                res["quantity"] = move.accepted_qty
            elif move.product_uom_acc_qty:
                res["quantity"] = move.product_uom_acc_qty
        return res


class StockPicking(models.Model):

    _inherit = "stock.picking"

    reviewed = fields.Boolean(string="Reviewed", default=False)
    payment_mode = fields.Many2one(
        'payment.mode',
        compute='_get_payment_mode',
        string='Payment Mode',
        store=False)
    # delivery_id = fields.Many2one(related='route_detail_id.comercial_id',
    #                                store=True, string='Delivery Person')
    # invoice_id = fields.Many2one()
    move_lines = fields.One2many('stock.move', 'picking_id',
                                 'Internal Moves',
                                 states={'done': [('readonly', False)],
                                         'cancel': [('readonly', True)]},
                                 copy=True)
    amount_untaxed_acc = fields.Float(
        compute='_amount_all_acc',
        digits_compute=dp.get_precision('Account'),
        string='Untaxed Amount Review', readonly=True, store=False)
    amount_tax_acc = fields.Float(
        compute='_amount_all_acc',
        digits_compute=dp.get_precision('Account'),
        string='Taxes Review', readonly=True, store=False)
    amount_total_acc = fields.Float(
        compute='_amount_all_acc',
        digits_compute=dp.get_precision('Account'),
        string='Total Review', readonly=True, store=False)
    amount_gross_acc = fields.Float(
        compute='_amount_all_acc',
        digits_compute=dp.get_precision('Account'),
        string='amount gross Review', readonly=True, store=False)
    amount_discounted_acc = fields.Float(
        compute='_amount_all_acc',
        digits_compute=dp.get_precision('Account'),
        string='Sale price', readonly=True, store=False)
    receipt_amount = fields.Float(
        compute='_receipt_amount',
        digits_compute=dp.get_precision('Account'),
        string='Receipt', readonly=False, store=False)

    @api.multi
    def _get_payment_mode(self):
        sale_obj = self.env["sale.order"]
        for picking in self:
            picking.payment_mode = False
            if picking.group_id:
                sale_ids = sale_obj.search([('procurement_group_id', '=',
                                             picking.group_id.id)])
                if sale_ids:
                    picking.payment_mode = sale_ids[0].payment_mode_id.id

    @api.multi
    def _receipt_amount(self):
        init_t = time.time()
        cash_type = self.env['ir.model.data'].\
            get_object_reference('stock_picking_review',
                                 'payment_mode_type_cash')
        cash_type_id = cash_type[1]
        for picking in self:
            if not picking.sale_id:
                picking.receipt_amount = 0.0
                continue
            else:
                if picking.sale_id.payment_mode_id.type.id == cash_type_id:
                    picking.receipt_amount = picking.amount_total_acc
        _logger.debug("CMNT _receipt_amount %s", time.time() - init_t)

    @api.multi
    def fast_returns(self):
        move_obj = self.env['stock.move']
        res = []
        for pick in self:
            # Cancel assignment of existing chained assigned move
            invoice_st = 'none'
            if pick.invoice_state in ['invoiced']:
                invoice_st = '2binvoiced'
            else:
                invoice_st = 'none'
            moves_to_unreserve = []
            if pick.picking_type_id.code != 'outgoing':
                raise except_orm(_('Error!'), _('Fast return'
                                                ' is only available with'
                                                ' outgoing pickings!'))
            for move in pick.move_lines:
                to_check_moves = [move.move_dest_id] if move.move_dest_id.id \
                    else []
                while to_check_moves:
                    current_move = to_check_moves.pop()
                    if current_move.state not in ('done', 'cancel') and \
                            current_move.reserved_quant_ids:
                        moves_to_unreserve.append(current_move.id)
                    split_move_ids = move_obj.search([('split_from', '=',
                                                       current_move.id)])
                    if split_move_ids:
                        to_check_moves += move_obj.browse(split_move_ids)

            if moves_to_unreserve:
                move_obj.do_unreserve(moves_to_unreserve)
                # break the link between moves in order to be able to fix
                # them later if needed
                move_obj.write(moves_to_unreserve, {'move_orig_ids': False})

            # Create new picking for returned products
            pick_type_id = pick.picking_type_id.return_picking_type_id and \
                pick.picking_type_id.return_picking_type_id.id or \
                pick.picking_type_id.id
            moves = self.env['stock.move']
            if pick.invoice_state in ['invoiced']:
                invoice_st = '2binvoiced'
            else:
                invoice_st = 'none'
            for move in pick.move_lines:
                new_qty = move.product_uos_qty - move.accepted_qty
                new_uom_qty = move.product_uom_qty - move.product_uom_acc_qty
                if pick.invoice_state == '2binvoiced' and \
                        pick.state in ['done'] and \
                        float_is_zero(move.product_uom_acc_qty, precision_digits=0):
                    # Si la cantidad aceptada es cero esta linea no debe
                    # facturarse
                    move.invoice_state = 'none'

                if new_uom_qty:
                    # The return of a return should be linked with
                    # the original's destination move if it was not cancelled
                    if move.origin_returned_move_id.move_dest_id.id and \
                            move.origin_returned_move_id.move_dest_id.state  \
                            != 'cancel':
                        move_dest_id = \
                            move.origin_returned_move_id.move_dest_id.id
                    else:
                        move_dest_id = False
                    if len(move.linked_move_operation_ids) == 1:
                        lot_id = \
                            move.linked_move_operation_ids[0].\
                            operation_id.lot_id and \
                            move.linked_move_operation_ids[0].\
                            operation_id.lot_id.id
                    else:
                        lot_id = False
                    # returned_lines += 1
                    new_move_id = move.copy({
                        'product_id': move.product_id.id,
                        'product_uom_qty': new_uom_qty,
                        'product_uos_qty': new_qty,
                        'picking_id': False,
                        'state': 'draft',
                        'accepted_qty': new_qty,
                        'product_uom_acc_qty': new_uom_qty,
                        'location_id': move.location_dest_id.id,
                        'location_dest_id': move.location_id.id,
                        'picking_type_id': pick_type_id,
                        'warehouse_id': pick.picking_type_id.warehouse_id.id,
                        'origin_returned_move_id': move.id,
                        'procure_method': 'make_to_stock',
                        'restrict_lot_id': lot_id,
                        'move_dest_id': move_dest_id,
                        'invoice_state': invoice_st
                    })
                    moves += new_move_id

            if len(moves):
                new_picking = pick.copy({
                    'move_lines': [],
                    'picking_type_id': pick_type_id,
                    'state': 'draft',
                    'origin': pick.name,
                    'task_type': 'ubication',
                    'invoice_id': False,
                    'invoice_state': invoice_st
                })
                res.append(new_picking.id)
                for move in moves:
                    move.picking_id = new_picking.id
                new_picking.action_confirm()
                new_picking.action_assign()

        self.write({'reviewed': True})
        return res

    @api.multi
    def _amount_all_acc(self):
        init_t = time.time()
        for picking in self:
            val1 = 0
            val = 0.0
            if picking.picking_type_id.code == "outgoing":
                if not picking.sale_id:
                    picking.amount_tax_acc = picking.amount_untaxed_acc = \
                        picking.amount_gross_acc = 0.0
                    continue

                cur = picking.partner_id.property_product_pricelist \
                    and picking.partner_id.property_product_pricelist.\
                    currency_id or False
                for line in picking.move_lines:
                    sale_line = line.procurement_id.sale_line_id
                    if sale_line and line.state != 'cancel':
                        price_unit = \
                            line.procurement_id.sale_line_id.price_unit
                        price_disc_unit = price_unit
                        price = price_disc_unit
                        qty = line.product_uom_acc_qty

                        val1 += line.price_subtotal_accepted
                        if sale_line and line.state != 'cancel':

                            partner_sale = sale_line.order_id.partner_id
                            res = sale_line.tax_id.\
                                compute_all(price, qty, line.product_id,
                                            partner_sale)['taxes']
                            for c in res:
                                val += c.get('amount', 0.0)
                    else:
                        continue
                if cur:
                    picking.amount_tax_acc = cur.round(val)
                    picking.amount_untaxed_acc = cur.round(val1)
                    # picking.amount_gross_acc = cur.round(amount_gross)
                else:
                    picking.amount_tax_acc = round(val, 2)
                    picking.amount_untaxed_acc = round(val1, 2)
                    # picking.amount_gross_acc = round(amount_gross, 2)

                picking.amount_total_acc = picking.amount_untaxed_acc + \
                    picking.amount_tax_acc
                # picking.amount_discounted_acc = picking.amount_gross_acc - \
                #    picking.amount_untaxed_acc
        print picking
        _logger.debug("CMNT Calculo en  _amount_all_acc (picking) %s",
                      time.time() - init_t)

    @api.cr_uid_ids_context
    def do_recompute_remaining_quantities(self, cr, uid, picking_ids,
                                          context=None):
        for picking in self.browse(cr, uid, picking_ids, context=context):
            if picking.pack_operation_ids and picking.state == 'done':
                return
        return super(StockPicking, self).\
            do_recompute_remaining_quantities(cr, uid, picking_ids, context)


class StockPackOperation(models.Model):
    _inherit = "stock.pack.operation"

    @api.one
    def unlink(self):
        if self.picking_id.state == 'done':
            return  # Avoid unlink operations in done state
        return super(StockPackOperation, self).unlink()
