# -*- coding: utf-8 -*-
# Copyright 2018 Kiko Sánchez, <kiko@comunitea.com> Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    grouped_field_ids = fields.Many2many('ir.model.fields', string='Albaranes agrupados por ...', domain=[('model_id.model', '=', 'stock.move')], help="Los movimientos se pueden agrupar por estos campos al crear un albarán.")
    grouped_batch_field_ids = fields.Many2many('ir.model.fields', string='Grupos agrupados por ....', domain=[('model_id.model', '=', 'stock.picking')], help="Los albaranes se pueden agrupar por estos campos al crear un grupo.")
    after_assign = fields.Boolean('Cancelar asignación directa', help="Se busca disponibilidad antes de asignar albarán.")
    batch_picking_sequence_id = fields.Many2one('ir.sequence', 'Secuencia de lote')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_batch_domain(self):

        self.ensure_one()
        domain = [('state', 'not in', ('done', 'cancel')),
                  ('picking_type_id', '=', self.picking_type_id.id)]

        if self._context.get('pick_domain', False):
            domain += self._context['pick_domain']

        for field in self.picking_type_id.grouped_batch_field_ids:
            if self[field.name]:
                if field.ttype == 'many2one':
                    domain += [(field.name, '=', self[field.name].id)]
                else:
                    domain += [(field.name, '=', self[field.name])]
        return domain


    def get_batch_vals(self):

        vals = {
                'picking_type_id': self.picking_type_id.id,
                'date': self.scheduled_date,
                }
        for field in self.picking_type_id.grouped_batch_field_ids:
            if self[field.name]:
                if field.ttype == 'many2one':
                    vals.update({field.name: self[field.name].id})
                #elif field.ttype == 'selection':
                #    vals.update({self[field.name]: self[field.name]})
                else:
                    vals.update({field.name: self[field.name]})

        return vals

    @api.multi
    def auto_assign_batch_picking(self, create=True):

        sbp = self.env['stock.batch.picking']
        for pick in self:
            domain = pick.get_batch_domain()
            b_id = sbp.search(domain, limit=1)
            if not b_id and create:
                b_id = sbp.create(pick.get_batch_vals())

            pick.batch_picking_id = b_id and b_id.id

class StockBatchPicking(models.Model):
    _inherit = 'stock.batch.picking'

    partner_id = fields.Many2one('res.partner', string='Empresa', compute='get_partner_id', store=True)

    name = fields.Char(
        'Name', default='/',
        required=True, index=True,
        copy=False, unique=True,
        states={'draft': [('readonly', False)]})

    @api.depends('picking_ids.partner_id')
    @api.multi
    def get_partner_id(self):
        for batch in self:
            if batch.state == 'done':
                partner_id = batch.picking_ids.mapped('partner_id')

            if len(partner_id) == 1:
                batch.partner_id = partner_id[0]
            else:
                batch.partner_id = False


    @api.model
    def create(self, vals):
        defaults = self.default_get(['name', 'picking_type_id'])
        picking_type_id = vals.get('picking_type_id', defaults.get('picking_type_id'))
        sequence_id = self.env['stock.picking.type'].browse(picking_type_id).batch_picking_sequence_id
        if vals.get('name', '/') == '/' and defaults.get('name', '/') == '/' and picking_type_id and sequence_id:
            vals['name'] = sequence_id.next_by_id()
        else:
            vals['name'] =  self.env['ir.sequence'].next_by_code('stock.batch.picking.lr')
        return super().create(vals)




