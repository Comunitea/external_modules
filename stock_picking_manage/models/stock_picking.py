# -*- coding: utf-8 -*-
# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class StockReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    to_refund = fields.Boolean(default=True)


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        for line in res.get('product_return_moves', []):
            line[2]['to_refund'] = True
        return res

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def action_draft(self):
        self.mapped('move_lines')._action_cancel()
        self.write({'is_locked': True})
        return True

    @api.multi
    def action_re_confirm(self):
        self.ensure_one()
        self.mapped('move_lines').filtered(lambda x:x.state == 'cancel').write({'state': 'draft'})
        if all(x.state=='draft' for x in self.move_lines):
            self.action_confirm()

    @api.multi
    def get_domain(self):
        my_categ= self.env.ref('stock_picking_manage.res_partner_delivery_carrier')
        if my_categ:
            domain = [('id', 'in', my_categ.partner_ids.ids)]
        else:
            domain = []
        return domain

    @api.multi
    def _count_product_ids(self):
        for pick in self:
            count = len(pick.move_line_ids.mapped('product_id'))
            pick.product_ids_count = count

    delivery_note = fields.Text('Delivery note')
    carrier_partner_id = fields.Many2one('res.partner', string="Carrier partner", domain=lambda self: self.get_domain())
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
        model = self._context.get('model_dest', 'stock.move')
        for picking in self:
            if model == 'move.line':
                picking.move_lines.force_set_qty_done()
            else:
                picking.move_line_ids.force_set_qty_done()

    @api.multi
    def action_done(self):
        return super().action_done()

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
