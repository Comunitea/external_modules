# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from time import time

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
# from odoo.tools.float_utils import float_compare
from odoo.addons.alternative_tracking.models.product_product import TRACKING_VALUES

_logger = logging.getLogger(__name__)

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.multi
    def _get_available_serial_ids(self):
        # Devuelve los números dee serie disponibles para este move_line
        spl = self.env["stock.lot"]
        for line in self.filtered(lambda x: x.template_tracking == 'virtual'):
            move_orig_ids = (line.move_id.origin_returned_move_id | line.move_id.move_orig_ids)
            location_id = line.location_id
            product_id = line.product_id
            # Si tiene moveimientos previosm entonces los series solo pueden ser de aquí y con ubicación en el mismo sitio
            if move_orig_ids:
                domain = [
                    ("location_id.serial_location", "=", location_id.serial_location.id),
                    ("id", "in", move_orig_ids.mapped("serial_ids").ids),
                ]
            else:
                domain = product_id.get_serial_domain(location_id=location_id)
            line.available_serial_ids = spl.search(domain)

    serial_ids = fields.Many2many(
        comodel_name="stock.lot",
        relation="serial_id_move_line_id_rel",
        column1="move_line_id",
        column2="serial_id",
        string="Lots",
        copy=False,
    )
    available_serial_ids = fields.One2many(
        "stock.lot", compute=_get_available_serial_ids
    )
    serial_name_ids = fields.One2many(
        comodel_name='virtual.serial',
        inverse_name="move_line_id",
        string="Future lots",
        help="Future lot ids, convert to lot when sml is done. Borrados en el action done")
    
    lot_ids_string = fields.Text("Serial list to add", help="Technical field to conver texto to serial_name_ids. Conver to serial_name_ids")
    # virtual_tracking = fields.Boolean(related='product_id.virtual_tracking', store=True)
    template_tracking = fields.Selection(related='product_id.product_tmpl_id.template_tracking') #, store=True)
    # tracking = fields.Selection(selection=TRACKING_VALUES, default='none')
    picking_type_id = fields.Many2one(related="move_id.picking_type_id")
    serial_location = fields.Many2one(related="location_id.serial_location")
    show_name_ids = fields.Boolean(string="Use barcode reader", default=True)


    def get_use_create_lots(self):
        picking_type_id = self.picking_type_id
        if picking_type_id:
            use_create_lots = picking_type_id and picking_type_id.use_create_lots 
        elif self.move_id.inventory_id:
            use_create_lots = True
        else:
            use_create_lots = False
        return use_create_lots

    def create_virtual_serial_from_list(self, lot_names):
        # Si lot_names es una cadena: Reemplazo los . y las , por retorno de carro y separo por lineas para hacer una lista
        lot_names = self.product_id.compute_names_from_string(lot_names, lot_names=self.serial_name_ids.mapped('name'))
        # Tengo que crear los virtual.serial
        for lot_name in lot_names:
            self.env['virtual.serial'].create({'name': lot_name, 'move_line_id': self.id})
        return True

    @api.onchange('serial_ids', 'serial_name_ids')
    def onchange_lot_ids(self):
        if self.state in ["done", "cancel", "draft"]:
            raise ValidationError(_("Incorrect move state"))
        if self.template_tracking == 'virtual' and not self._context.get("by_pass_compute_qties", False):
            self.qty_done = len(self.serial_ids) + len(self.serial_name_ids) 

    @api.multi
    def action_alternative_tracking_in_move_line(self):
        self.ensure_one()
        # if self.get_use_create_lots():
        #  view = self.env.ref("alternative_tracking.stock_move_line_tracking_form_tree_serial")
        # else:
        view = self.env.ref("alternative_tracking.stock_move_line_tracking_form_tree_serial")
        return {
            "name": _("Tracking Form Operations"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "stock.move.line",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": self.id,
        }

    @api.multi
    def action_open_tracking_form(self):
        self.ensure_one()
        view = self.env.ref("alternative_tracking.stock_move_line_tracking_form")
        return {
            "name": _("Tracking Form Operations"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "stock.move.line",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": self.id,
        }

    @api.multi
    def write(self, vals):
        if vals.get('lot_ids_string', False):
            lot_names = self.env['stock.move.line'].product_id.compute_names_from_string(vals['lot_ids_string'])
            vals['lot_ids_string'] = ",".join(lot_names)
        res = super().write(vals)
        if 'qty_done' not in vals and len(self) == 1:
            if 'serial_ids' in vals:
                self.qty_done = len(self.serial_ids)
            elif 'serial_name_ids' in vals:
                self.qty_done = len(self.serial_name_ids)
        return res

    def write_serial_location(self):
        sml_ids = self.filtered(lambda x: x.state == 'done')
        for sml_id in sml_ids:
            location_id = sml_id.location_dest_id.serial_location or sml_id.location_dest_id
            sml_id.serial_ids.write({
                'serial_location': sml_id.location_dest_id.id,
                'location_id': location_id.id
            })

    def filter_affected_moves(self):
        # Los movimientos afectados son:
        return self.filtered(lambda x: 
                                x.state != 'done' 
                                and x.template_tracking == 'virtual'
                                and not x.move_id.inventory_id  # Los que vengan de un inventario
                                and not x.picking_type_id.bypass_tracking  # tipo de albarán arcado para ignorarlos
                                and not (x.move_id.raw_material_production_id or x.move_id.production_id)  # Los que vengan de producciones.
                            )

    def _action_done(self):
        # Todoso los serial_virtual deben convertirse a serial antes de llegar aquí
        affected_moves = self.filter_affected_moves()
        res = super()._action_done()
        virtual_tracking_move_ids = affected_moves.filtered(lambda x: x.qty_done > 0)
        if not virtual_tracking_move_ids:
            return res
        # use_create_lots = virtual_tracking_move_ids[0].get_use_create_lots()
        bypass_serial_error_location = virtual_tracking_move_ids[0].picking_type_id and virtual_tracking_move_ids[0].picking_type_id.bypass_serial_error_location or False
        check_serial_qties = virtual_tracking_move_ids[0].picking_type_id and virtual_tracking_move_ids[0].picking_type_id.check_serial_qties or True
        for sml_id in virtual_tracking_move_ids:
            if (not sml_id.serial_ids):
                raise ValidationError(_("You need serial numbers"))
            if not bypass_serial_error_location:
                if any(x.serial_location for x in sml_id.serial_ids != sml_id.location_id.serial_location):
                    raise ValidationError(_("Incorrect serial location"))
            if check_serial_qties:
                if len(sml_id.serial_ids) != sml_id.qty_done:
                    raise ValidationError(_('Incorrect serial quantity vs qty done'))

        virtual_tracking_move_ids.write({'show_name_ids': True})
        virtual_tracking_move_ids.write_serial_location()
        return res

    def create_serial_ids_from_serial_names(self):

        for sml_id in self:
            bypass_serial_error_location = sml_id.picking_type_id and sml_id.picking_type_id.bypass_serial_error_location or False
            use_create_lots = sml_id.get_use_create_lots()
            if sml_id.state == 'done':
                location = sml_id.location_dest_id
            else:
                location = sml_id.location_id

            to_add = self.env['stock.lot']
            product_id = sml_id.product_id 
            if not bypass_serial_error_location:
                if any(x.serial_location for x in sml_id.serial_name_ids != location.serial_location):
                    raise ValidationError(_("Incorrect serial location"))
            for serial_name in sml_id.serial_name_ids:
                domain = [
                    ('name', '=', serial_name.name), 
                    ('product_id', '=', product_id.id),
                    '|', ('active', '=', True), ('active', '=', False)]

                serial_id = self.env['stock.lot'].search(domain, limit=1)
                if serial_id:
                    if not serial_id.active:
                        serial_id.active = True
                    to_add += serial_id
                else:
                    if not use_create_lots:
                        raise ValidationError(_('This type not allow create serial numbers'))
                    serial_vals = {
                        "product_id": product_id.id,
                        "serial_location": location.serial_location.id,
                        "location_id": location.id,
                        "name": serial_name.name,
                        "ref": serial_name.name
                    }
                    to_add += self.env['stock.lot'].create(serial_vals)
            sml_id.write({'serial_ids': [(4, val) for val in to_add.ids]})