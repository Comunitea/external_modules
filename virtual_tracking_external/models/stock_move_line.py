# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from time import time

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
# from odoo.tools.float_utils import float_compare
from odoo.addons.virtual_tracking.models.product_product import TRACKING_VALUES

_logger = logging.getLogger(__name__)

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    serial_ids = fields.Many2many(
        comodel_name="stock.lot",
        relation="serial_id_move_line_id_rel",
        column1="move_line_id",
        column2="serial_id",
        string="Lots",
        copy=False,
    )
    available_serial_ids = fields.One2many(related='move_id.available_serial_ids')
    # Lo sustituyo por lot_name
    serial_ids_string = fields.Text("Serial list to add", help="Technical field to conver texto to serial_ids")
    # virtual_tracking = fields.Boolean(related='product_id.virtual_tracking', store=True)
    template_tracking = fields.Selection(related='product_id.product_tmpl_id.template_tracking') #, store=True)
    # tracking = fields.Selection(selection=TRACKING_VALUES, default='none')
    # picking_type_id = fields.Many2one(related="move_id.picking_type_id")

    def get_use_create_lots(self):
        picking_type_id = self.move_id.picking_type_id
        if picking_type_id:
            use_create_lots = picking_type_id and picking_type_id.use_create_lots 
        elif self.move_id.inventory_id:
            use_create_lots = True
        else:
            use_create_lots = False
        return use_create_lots

    @api.onchange('serial_ids')
    def onchange_lot_ids(self):
        if self.state in ["done", "cancel", "draft"]:
            raise ValidationError(_("Incorrect move state"))
        if self.template_tracking == 'virtual' and not self._context.get("by_pass_compute_qties", False):
            self.qty_done = len(self.serial_ids)

    def action_alternative_tracking_in_move_line(self):
        self.ensure_one()
        # if self.get_use_create_lots():
        #  view = self.env.ref("virtual_tracking.stock_move_line_tracking_form_tree_serial")
        # else:
        view = self.env.ref("virtual_tracking.stock_move_line_tracking_form_tree_serial")
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

    def action_open_tracking_form(self):
        self.ensure_one()
        view = self.env.ref("virtual_tracking.stock_move_line_tracking_form")
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

    def write(self, vals):
        if len(self) == 1 and vals.get('serial_ids_string', False):
            serial_names = self.product_id.sanitize_lot_names(vals['serial_ids_string'])
            vals['serial_ids_string'] = ",".join(serial_names)
            if not 'qty_done' in vals:
                vals['qty_done'] = len(vals['serial_ids_string'])
        res = super().write(vals)
        if 'qty_done' not in vals and len(self) == 1:
            if 'serial_ids' in vals:
                self.qty_done = len(self.serial_ids)
        return res

    def write_serial_location(self):
        for sml_id in self:
            sml_id.serial_ids.write({'location_id': sml_id.location_dest_id.serial_location_id.id})

    def filter_affected_moves(self):
        # Los movimientos afectados son:
        return self.filtered(lambda x: 
                                x.state != 'done' 
                                and x.template_tracking == 'virtual'
                                # and not x.move_id.inventory_id  # Los que vengan de un inventario
                                and not x.move_id.picking_type_id.bypass_tracking  # tipo de albarán arcado para ignorarlos
                                and not (x.move_id.raw_material_production_id or x.move_id.production_id)  # Los que vengan de producciones.
                            )

    def _action_done(self):
        # Todoso los serial_virtual deben convertirse a serial antes de llegar aquí
        affected_moves = self.filter_affected_moves()
        if affected_moves:
            affected_moves.filtered(lambda x: x.serial_ids_string).convert_serial_ids_string_to_serial_ids()
            # compruebo 
            picking_type_id = affected_moves[0].move_id.picking_type_id
            if picking_type_id:
                bypass_serial_error_location = picking_type_id.bypass_serial_error_location
                check_serial_qties = picking_type_id.check_serial_qties
            else:
                bypass_serial_error_location = False
                check_serial_qties = True

            for sml_id in affected_moves:
                if check_serial_qties and sml_id.qty_done != len(sml_id.serial_ids):
                    raise ValidationError(_('Incorrect serial quantity vs qty done'))
                if not bypass_serial_error_location:
                    if any(x.location_id != sml_id.location_id.serial_location_id for x in sml_id.serial_ids):
                        raise ValidationError(_("Incorrect serial location"))

        res = super()._action_done()
        affected_moves.filtered(lambda x: x.serial_ids).write_serial_location()
        return res

    def convert_serial_ids_string_to_serial_ids(self):
        for sml_id in self:
            lot_names = sml_id.product_id.sanitize_lot_names(sml_id.serial_ids_string)
            if not lot_names:
                continue
            serial_location_id = sml_id.location_id.serial_location_id
            location = sml_id.location_id
            bypass_serial_error_location = sml_id.picking_type_id and sml_id.picking_type_id.bypass_serial_error_location or False
            
            use_create_lots = sml_id.get_use_create_lots()
           
            to_add = self.env['stock.lot']
            product_id = sml_id.product_id
            domain = [
                    ('name', 'in', lot_names), 
                    ('product_id', '=', product_id.id)]
                    # '|', ('active', '=', True), ('active', '=', False)]
            existing_serial_ids = self.env['stock.lot'].search(domain)
            if not bypass_serial_error_location:
                # Tengo que comprobar la ubicación de los números de serie que existan
                if any(x.location_id != serial_location_id for x in existing_serial_ids):
                    raise ValidationError(_("Incorrect serial location"))

            for serial_name in lot_names:
                serial_id = existing_serial_ids.filtered(lambda x: x.name == serial_name)
                if serial_id:
                    # if not serial_id.active:
                    #    serial_id.active = True
                    if serial_id.location_id != location:
                        # Si no se puede hay un raise antes
                        serial_id.location_id = location
                    to_add += serial_id
                    _logger.info("Linkeado Serial %s" %serial_name)
                else:
                    if not use_create_lots:
                        raise ValidationError(_('This type not allow create serial numbers'))
                    serial_vals = {
                        "product_id": product_id.id,
                        "location_id": location.id,
                        "name": serial_name,
                    }
                    to_add += self.env['stock.lot'].create(serial_vals)
                    _logger.info("Creado Serial %s" %serial_name)
            sml_id.write({'serial_ids_string': False, 'serial_ids': [(4, val) for val in to_add.ids]})