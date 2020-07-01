# -*- coding: utf-8 -*-

from odoo import _, api, models, fields
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import time
import pprint
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class StockPickingBatch(models.Model):

    _inherit = ['info.apk', 'stock.picking.batch']
    _name = 'stock.picking.batch'

    @api.multi
    def compute_apk_name(self):
        for obj in self:
            obj.apk_name = obj.name

    @api.multi
    def compute_move_line_count(self):
        for pick in self:
            pick.move_line_count = len(pick.move_line_ids)

    @api.multi
    def compute_total_reserved_availability(self):
        for pick in self:
            pick.total_reserved_availability = sum(x.reserved_availability for x in pick.move_lines)

    app_integrated = fields.Boolean(related='picking_type_id.app_integrated')
    move_line_count = fields.Integer('# Operaciones', compute="compute_move_line_count")
    total_reserved_availability = fields.Integer('# Cantidad', compute="compute_total_reserved_availability")
    field_status = fields.Boolean(compute="compute_field_status")
    default_location = fields.Selection(related='picking_type_id.group_code.default_location')
    group_code = fields.Selection(related='picking_type_id.group_code.code')
    barcode_re = fields.Char(related='picking_type_id.warehouse_id.barcode_re')
    product_re = fields.Char(related='picking_type_id.warehouse_id.product_re')
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', compute='_compute_picking_type_id', store = True)
    scheduled_date = fields.Datetime(
        'Scheduled Date', compute='_compute_scheduled_date')
    sale_ids = fields.One2many('sale.order', string='Ventas', compute="_compute_order_ids")
    sale_id = fields.Many2one('sale.order', string='Venta', compute="_compute_order_ids")
    purchase_ids = fields.One2many('purchase.order', string='Compras', compute="_compute_order_ids")
    purchase_id = fields.Many2one('purchase.order', string='Compra', compute="_compute_order_ids")
    location_id = fields.Many2one(related="picking_type_id.default_location_src_id")
    location_dest_id = fields.Many2one(related="picking_type_id.default_location_dest_id")
    priority = fields.Selection (related='picking_ids.priority')
    pick_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_pick_state')


    @api.multi
    def _compute_pick_state(self):

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
        for batch in self:
            if not batch.picking_ids:
                batch.pick_state = 'draft'
            elif any(pick.state == 'draft' for pick in batch.picking_ids):  # TDE FIXME: should be all ?
                batch.pick_state = 'draft'
            elif all(pick.state == 'cancel' for pick in batch.picking_ids):
                batch.pick_state = 'cancel'
            elif all(pick.state in ['cancel', 'done'] for pick in batch.picking_ids):
                batch.pick_state = 'done'
            elif any(pick.state in ['waiting', 'confirmed'] for pick in batch.picking_ids):
                batch.pick_state = 'confirmed'
            elif all(pick.state == 'assigned' for pick in batch.picking_ids):  # TDE FIXME: should be all ?
                batch.pick_state = 'assigned'
            else:
                batch.pick_state = 'draft'

    @api.one
    @api.depends('picking_ids.picking_type_id')
    def _compute_picking_type_id(self):
        self.picking_type_id = self.picking_ids.mapped('picking_type_id')

    @api.multi
    def _compute_order_ids(self):
        for batch in self:
            batch.sale_ids = batch.picking_ids.mapped('sale_id')
            if batch.sale_ids:
                batch.sale_id = batch.sale_ids[0]
            batch.purchase_ids = batch.picking_ids.mapped('purchase_id')
            if batch.purchase_ids:
                batch.purchase_id = batch.purchase_ids[0]

    @api.multi
    def _compute_scheduled_date(self):
        for batch in self:
            batch.scheduled_date = min(batch.move_lines.mapped('date_expected') or [fields.Datetime.now()])
    @api.multi
    def compute_field_status(self):
        for pick in self:
            pick.field_status = all(x.field_status == True for x in pick.move_lines)


    def return_fields(self, mode='tree'):
        res = ['id', 'apk_name', 'location_id', 'location_dest_id', 'scheduled_date',
               'pick_state', 'sale_id', 'move_line_count', 'picking_type_id', 'purchase_id', 'total_reserved_availability',
               'default_location', 'field_status', 'priority']
        if mode == 'form':
            res += ['field_status', 'group_code', 'barcode_re', 'product_re', 'sale_ids', 'purchase_ids']
        return res

    def _compute_picking_count_domains(self):
        # DEBE SER UNA COPIA DE LOS DOMINIOS QUE SE USAN PARA CALCULAR LOS VALORES
        domains = {
            'count_picking_draft': [('state', '=', 'draft')],
            'count_picking_waiting': [('state', 'in', ('confirmed', 'waiting'))],
            'count_picking_ready': [('state', '=', 'assigned')],
            'count_picking': [('state', 'in', ('assigned', 'waiting', 'confirmed'))],
            'count_picking_late': [('date', '<', time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)), ('state', 'in', ('assigned', 'waiting', 'confirmed'))],
            'count_picking_backorders': [('backorder_id', '!=', False), ('state', 'in', ('confirmed', 'assigned', 'waiting'))],
        }
        return domains

    @api.model
    def get_picking_list(self, values):
        domain = []
        if values.get('picking_type_id', False):
            domain += [('picking_type_id', '=', values['picking_type_id'])]
        if values.get('state', False):
            domain += [('state', '=', values['state']['value'])]
        elif values.get('domain_name', False):
            domain += self._compute_picking_count_domains()[values['domain_name']]
        if values.get('search', False):
            domain += [('name', 'ilike', values['search'] )]

        if not domain and values.get('active_ids'):
            domain += [('id', 'in', values.get['active_ids'])]
        values['domain'] = domain
        ## Cambio el valor de dominio por ids de picking
        batch_ids = self.env['stock.picking'].search(domain).mapped('batch_id').ids
        values['domain'] = [('id', 'in', batch_ids)]
        return self.get_model_object(values)


    def get_move_domain_for_picking(self, filter, batch_id, inc=0, limit = 0, apk_order = -1):
        sql = "select move_id from stock_move_line sml " \
              "join stock_move sm on sm.id = sml.move_id " \
              "join stock_picking sp on sp.id = sml.picking_id " \
              "where sp.batch_id = {}".format(batch_id.id)
        if filter == 'Pendientes':
            sql += " and qty_done != sml.product_uom_qty"
        if filter == 'Completados':
            sql += " and qty_done == sml.product_uom_qty"
        order = ''
        #if apk_order > 0:
        if inc == -1:
            if apk_order > -1: sql += " and sm.apk_order < {}".format(apk_order)
            order = ' order by sm.apk_order desc'
        else:
            if apk_order > -1: sql += " and sm.apk_order > {}".format(apk_order)
            order = ' order by sm.apk_order asc'
        sql += " group by move_id, sm.apk_order "
        if order:
            sql += order
        if limit > 0:
            sql += ' limit {}'.format(limit)
        # sql += " group by move_id"
        self._cr.execute(sql)
        move_ids = self._cr.fetchall()
        if move_ids:
            if len(move_ids) > 1:
                res_ids = [x[0] for x in move_ids]
                domain = [('id', 'in', res_ids)]
            else:
                domain = [('id', '=', move_ids[0][0])]
        else:
            domain = [('id', '=', 0)]
        return domain

    def assign_order_moves(self):
        cont = 1
        field_location = self.picking_type_id.group_code.default_location or 'location_id'
        self.move_lines.filtered(lambda x: not x.move_line_ids).write({'apk_order': 0})
        for move in self.move_line_ids.sorted(key=lambda r: r[field_location].removal_priority).mapped('move_id'):
            move.apk_order = cont
            cont += 1

    def get_model_object(self, values={}):
        res = super().get_model_object(values=values)
        picking_id = self
        if values.get('view', 'tree') == 'tree':
            return res
        if picking_id:
            picking_id.state == 'in_progress'
            picking_id.user_id = self.env.user
        if not picking_id:
            domain = values.get('domain', [])
            limit = values.get('limit', 1)
            move_id = self.search(domain, limit)
            if not picking_id or len(picking_id) != 1:
                return res
        values = {'domain': self.get_move_domain_for_picking(values.get('filter_moves', 'Todos'), picking_id)}
        res['move_lines'] = self.env['stock.move'].get_model_object(values)
        #print ("------------------------------Move lines")
        #pprint.PrettyPrinter(indent=2).pprint(res['move_lines'])
        return res

    @api.model
    def action_assign_apk(self, vals):
        picking = self.browse(vals.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán"}
        for pick in picking.picking_ids:
            pick.action_assign()
        return True

    @api.model
    def do_unreserve_apk(self, vals):
        picking = self.browse(vals.get('id', False))
        if not picking:
            return {'err': True, 'error': "No se ha encontrado el albarán"}
        for pick in picking.picking_ids:
            pick.do_unreserve()
        return True


    def check_allow_pda_validation(self):
        if any(x.location_id.usage == 'view' for x in self.move_line_ids):
            raise ValidationError('No puedes poner una cantidad en un aubicación de tipo vista')


    @api.model
    def button_validate_apk(self, vals):
        batch_id = self.browse(vals.get('id', False))
        if not batch_id:
            raise ValidationError ("No se ha encontrado el albarán")
        if all(move_line.qty_done == 0 for move_line in batch_id.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel'))):
            batch_id.message_post("No hay ninguna cantidad parta validar")
            return False
        if batch_id.check_allow_pda_validation():
            batch_id.message_post("No se a superado la validación incial del inventario")
            return False
        ctx = batch_id._context.copy()
        ctx.update(skip_overprocessed_check=True)
        for pick in batch_id.picking_ids:
            pick.with_context(ctx).action_done()
        return batch_id.get_model_object({'view': 'form'})

    @api.model
    def force_set_qty_done_apk(self, vals):
        picking_id = self.browse(vals.get('id', False))
        field = vals.get('field', False)
        if not picking_id:
            return {'err': True, 'error': "No se ha encontrado el albarán."}
        ctx = self._context.copy()
        ctx.update(model_dest="stock.move.line")
        ctx.update(field=field)
        for pick in picking_id.picking_ids:
            pick.with_context(ctx).force_set_qty_done()
        return True

    @api.model
    def force_reset_qties_apk(self, vals):
        picking_id = self.browse(vals.get('id', False))
        if not picking_id:
            return {'err': True, 'error': "No se ha encontrado el albarán."}
        ctx = self._context.copy()
        ctx.update(reset=True)
        for pick in picking_id.picking_ids:
            pick.with_context(ctx).force_set_qty_done()
        return True

    @api.model
    def process_qr_lines(self, vals):
        qr_codes = self.browse(vals.get('qr_codes', False))
        if not qr_codes:
            return {'err': True, 'error': "No se han recibido datos del código QR."}
        print(qr_codes)
        return True

    @api.model
    def find_pick_by_name(self, vals):
        domain = [('name', 'ilike', vals['name'])]
        res = self.search_read(domain, ['id'], limit=1)
        if res:
            print("------------- Busco el albarán {} y devuelvo  el id".format(vals['name'], res[0]['id']))
            return res[0]['id']
        print("------------- Busco el albarán {} y no encuentro nada".format(vals['name']))
        return False

    @api.model
    def find_serial_for_move(self, vals):
        # En esta funciuón miro si es un serial, si no busco en el barcode o en el wh_code a ver si encuentro un producto
        lot_name = vals.get('lot_id', False)
        picking_id = vals.get('picking_id', False)
        remove = vals.get('remove', False)
        if not picking_id:
            return
        if not lot_name:
            return

        ## Miro si es un lote o varios
        move = False

        lot_names = lot_name.split(',')
        moves_to_recompute = self.env['stock.move']
        for lot_name in lot_names:
            lot = self.env['stock.production.lot'].search([('name', '=', lot_name)], limit=1)
            if lot:
                move = self.serial_for_move(picking_id, lot, remove)
            if move:
                moves_to_recompute |= move
        if moves_to_recompute:
            moves_to_recompute._recompute_state()
            return move.get_model_object()

        ## NO se han encontrado numeros de serie, miro si es un producto.
        domain = [('picking_id.batch_id', '=', picking_id), ('product_id.tracking', '=', 'none') , '|', ('product_id.wh_code', '=', lot_name), ('product_id.barcode', '=', lot_name)]
        move_line_id = self.env['stock.move.line'].search(domain)
        if not move_line_id:
            raise ValidationError ('No se ha encontrado nada para el código {}'.format(lot_name))
        if len(move_line_id)>1:
            raise ValidationError('Se han encontrado varias opciones. No hay info suficiente para el código {}'.format(lot_name))
        values = {
            'move_id': move_line_id.move_id.id,
            'filter_moves': vals.get('filter_moves', 'Todos'),
            'location_id': move_line_id.location_id.id,
            'inc': 1}
        return move_line_id.move_id.set_qty_done_from_apk(values)


    @api.model
    def serial_for_move(self, picking_id, lot, remove):
        lot_id = lot.id
        product_id = lot.product_id.id
        new_location_id = lot.compute_location_id()
        domain = [('picking_id.batch_id', '=', picking_id), ('product_id', '=', product_id)]

        if False and remove:
            domain += [('lot_id', '=', lot_id)]
            line = self.env['stock.move.line'].search(domain, limit=1, order='lot_id desc')

            line.qty_done = 0
            line.write_status('lot_id', 'done', False)
            line.write_status('qty_done', 'done', False)
        else:
            # caso 1. COnfirmar el lote que hay
            lot_domain = domain + [('lot_id', '=', lot_id)]
            line = self.env['stock.move.line'].search(lot_domain, limit=1, order='lot_id desc')

            if line:
                ## si es lote +1 , si es serial = 1
                if line.product_id.tracking == 'serial':
                    line.qty_done = 1
                else:
                    line.qty_done += 1
                line.write_status('lot_id', 'done', True)
                line.write_status('qty_done', 'done', True)
            else:
                # Caso 2. Hay una vacía con lot_id = False:
                lot_domain = domain + [('lot_id', '=', False)]
                line = self.env['stock.move.line'].search(lot_domain, limit=1, order= 'lot_id desc')
                if not line:
                    lot_domain = domain + [('lot_id', '!=', lot_id), ('qty_done', '=', 0)]
                    line = self.env['stock.move.line'].search(lot_domain, limit=1, order='lot_id desc')
                if line:
                    move = line.move_id
                    line.unlink()
                    reserved = move._update_reserved_quantity(1, 1, location_id=move.location_id, lot_id=lot, strict=False)
                    if reserved == 0:
                        ocup_dom = [('move_id.picking_type_id', '=', move.picking_type_id.id),
                                    ('product_id', '=', move.product_id.id),
                                    ('state', 'in', ('assigned', 'partially_available')),
                                    ('lot_id', '=', lot_id)]
                        ocup_move_line = self.env['stock.move.line'].search(ocup_dom)
                        if ocup_move_line:
                            move_to_update = ocup_move_line.move_id
                            ocup_move_line.unlink()
                            reserved = move._update_reserved_quantity(1, 1, move.location_id, lot_id=lot, strict=False)
                            if move_to_update._update_reserved_quantity(1, 1, move.location_id, strict=False) == 1:
                                move_to_update.write({'state': 'assigned'})
                            if reserved == 0:
                                raise UserError ('No se ha podido reservar el lote {}. Comprueba que no está en otro movimiento'.format(lot.name))
                            move.write({'state': 'assigned'})

                    lot_domain = domain + [('lot_id', '=', lot_id)]
                    line = self.env['stock.move.line'].search(lot_domain, limit=1, order='lot_id desc')
                    if line:
                        line.qty_done = 1
                        line.write_status('lot_id', 'done', True)
                        line.write_status('qty_done', 'done', True)
        move = line.move_id
        if not move.picking_type_id.allow_overprocess and move.quantity_done > move.product_uom_qty:
            raise ValidationError("No puedes procesar más cantidad de lo reservado para el movimiento")
        ##devuelvo un objeto movimietno para actualizar la vista de la app
        if not move:
            return False
        return move






