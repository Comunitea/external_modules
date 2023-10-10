# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)
import re

TRACKING_VALUES = [
        ('virtual', 'Nº Serie Virtual'),
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')]

TO_REPLACE = ['/r/n', '/n', '/r', ',', '.']

class ForbiddenSerialName(models.Model):
    _name = "forbidden.serial.name"

    name = fields.Char('Name')
    product_id = fields.Many2one('product.product', string='Product')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_tracking_count(self):
        for templ_id in self:
            templ_id.tracking_count = sum(x.tracking_count for x in self.product_variant_ids)

    @api.depends('tracking', 'virtual_tracking')
    def _compute_template_tracking(self):
        for template in self:
            if template.virtual_tracking:
                template.template_tracking = 'virtual'
            else:
                template.template_tracking = template.tracking

    virtual_tracking = fields.Boolean(
        "With tracking", help="Alternative tracking for products with tracking = 'none'"
    )
    tracking_count = fields.Integer("Tracking serial count", compute=_compute_tracking_count)
    template_tracking = fields.Selection(
        selection=TRACKING_VALUES,
        string='Product Tracking', 
        compute=_compute_template_tracking, 
        store=True)
    
    forbidden_serial_ids = fields.One2many('forbidden.serial.name', 'product_id', string='Not valid serial names')

    def write(self, vals):
        tracking = vals.get('tracking', False)
        if tracking and tracking != 'none':
            vals['virtual_tracking'] = False
        return super().write(vals)

    def create(self, vals):
        tracking = vals.get('tracking', False)
        if tracking and tracking != 'none':
            vals['virtual_tracking'] = False
        return super().create(vals)

    def action_view_serials(self):
        action = self.env.ref("stock.action_production_lot_form").read()[0]
        action["context"] = {"product_id": self.id}
        domain = self.product_variant_ids.get_serial_domain()
        res = self.env["stock.lot"].search_read(domain, ["id"])
        action['context'] = {
            'default_product_id': self.product_variant_ids[0].id,
            'default_virtual_tracking': self.virtual_tracking}
        if res:
            ids = [x["id"] for x in res]
            action["domain"] = [("id", "in", ids)]
        else:
            action["domain"] = [('id', 'in', [])]
        return action

    @api.onchange("tracking")
    def onchange_tracking(self):
        self.virtual_tracking = False
        return super().onchange_tracking()


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_tracking_count(self):
        tracking_ids = self.filtered(lambda x: x.template_tracking != 'none')
        for product_id in tracking_ids:
            domain = product_id.get_serial_domain()
            product_id.tracking_count = self.env["stock.lot"].search_count(
                domain
            )
        (self - tracking_ids).write({'tracking_count': 0})

    tracking_count = fields.Integer("Tracking serial count", compute=_compute_tracking_count)
    reg_exp = fields.Char('Regular expression', help="Patron de expresiones regulares para los lotes o números de serie para una cadena de x caracteres(numeros y letras) y que empieza por ABC re.compile('^ABC[A-Za-z0-9]{x}$')")
    
    def action_view_serials(self):
        action = self.env.ref("stock.action_production_lot_form").read()[0]
        domain = self.get_serial_domain()
        res = self.env["stock.lot"].search_read(domain, ["id"])
        action['context'] = {
            'default_product_id': self.id,
            'default_virtual_tracking': self.virtual_tracking
        }
        if res:
            ids = [x["id"] for x in res]
            action["domain"] = [("id", "in", ids)]
        else:
            action["domain"] = [('id', 'in', [])]
        return action
    
    # Esta función devuelve los nº de serie  disponibles en una ubicación para un artículo
    def get_serial_domain(self, location_id=False, warehouse_id=False, lot_names=[], strict='='):
        n_prod = len(self)
        if not n_prod:
            domain = []
        elif n_prod == 1:
            domain = [('product_id', '=', self.id)]
        else:
            domain = [('product_id', 'in', self.ids)]
        if lot_names:
            domain = expression.AND([domain, [("name", "in", lot_names)]])
        if strict == 'all':
            return domain
        if not location_id:
            if warehouse_id:
                location_id = warehouse_id.lot_stock_id
            else:
                location_id = self.env.ref('stock.stock_location_stock')
        domain = expression.AND([domain, [("location_id", strict, location_id.serial_location.id)]])
        return domain

    def compute_names_from_string(self, lot_names, apply_regexp=True, product_id=False, move_line_id=False):
        if not lot_names:
            return []
        # Si lot_names es una cadena: Reemplazo los . y las , por retorno de carro y separo por lineas para hacer una lista
        if type(lot_names) is str:
            for signo in TO_REPLACE:
                lot_names = lot_names.replace(signo, ";")
            # Lo convierto a lista
            lot_names = lot_names.split(";")
        
        # Si no es una lista fallo
        if not (type(lot_names) is list):
            _logger.info("%s no es una lista" % lot_names)
            raise ValidationError(_("Values in unknown format"))
        
        # CONVIERTO A MAYUSCULAS?
        if self.env.user.company_id.serial_to_upper_case:            
            if lot_names:
                lot_names = [x.upper() for x in lot_names]

        # Si no hay producto, salgo aquí, solo lo convierto a una lista
        if not product_id:
            # Elimino duplicados de la lista
            set_list = set(lot_names)
            # Elimino vacios
            lot_names = list(set_list - {''})
            return lot_names
   
        # Miro si tengo que aplicar Expresiones regulares. Lo normal es que si
        if not apply_regexp and 'apply_regexp' in self._context:
            apply_regexp = self._context.get("apply_regexp", True)

   
        not_lot_names = []
        if product_id.not_lot_name_ids:
            not_lot_name = product_id.not_lot_name_ids.mapped('regexp')
        
        # ademas, para evitar los repetidos y ya leidos en ese albarán, aunque en otras líneas
        other_moves = self[0].move_id.picking_id.move_line_ids.filtered(lambda x: x.product_id == self.product_id)
        if other_moves:
            not_lot_name += other_moves.mapped('serial_ids.name')
        else:
            not_lot_name += self.mapped('serial_ids.name')

        # Revisar esto
            if self.serial_name_ids:
                not_lot_name += self.mapped('serial_name_ids.name')

        res = []
        for lot in lot_names:
            if lot is None:
                continue
            lot = lot.strip()
            
            if len(lot) < 3:
                continue
            if lot in not_lot_name:
                continue
            if lot in res:
                continue

            """
            EJEMPLO DE EXPRESION REGULAR: 
                re.match(expresion_regular, texto_a chequear, flags=re.IGNORECASE)
                
            if apply_regexp 
                and product_id.serial_regexp 
                and re.match('%'%product_id.serial_regexp, lot, flags=re.IGNORECASE):
            """

            if apply_regexp and self.product_id.serial_regexp:
                if not re.match('%s' % self.product_id.serial_regexp, lot):  # , flags=re.IGNORECASE)
                    continue
            res.append(lot)
        return sorted(res)