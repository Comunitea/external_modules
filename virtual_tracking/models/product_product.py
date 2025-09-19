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
        ('virtual', 'By Virtual Serial Number'),
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')]

TO_REPLACE = ['/r/n', '/n', '/r', ',', '.']



class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_tracking_count(self):
        for templ_id in self:
            templ_id.tracking_count = sum(x.tracking_count for x in self.product_variant_ids)

    template_tracking = fields.Selection(
        TRACKING_VALUES,
        string="Tracking", required=True, default='none', # Not having a default value here causes issues when migrating.
        compute='_compute_template_tracking', inverse="_inverse_template_tracking", store=True, readonly=False, precompute=True,
        help="Ensure the traceability of a storable product in your warehouse.")
    virtual_tracking = fields.Boolean(
        "With tracking", help="Alternative tracking for products with tracking = 'none'"
    )
    tracking_count = fields.Integer(
        "Tracking serial count", compute=_compute_tracking_count
    )
    template_tracking = fields.Selection(selection=TRACKING_VALUES, string='Product Tracking')

    @api.depends('is_storable')
    def _compute_template_tracking(self):
        self.filtered(lambda t: not t.is_storable and t.tracking != 'none').tracking = 'none'

    def _inverse_template_tracking(self):
        for templ in self:
            if templ.template_tracking == 'virtual':
                templ.virtual_tracking = True
                templ.tracking = 'none'
            else:
                templ.virtual_tracking = False
                templ.tracking = templ.template_tracking

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

class ProductProduct(models.Model):
    _inherit = "product.product"


    def _compute_reg_exp(self):
        for product_id in self:
            barcode = self.env['stock.lot'].search([('product_id', '=', product_id.id)], limit=1,order="id desc")
            if barcode:
                long = len(barcode.name)
                product_id.reg_exp = 	'^.{%d}$' %long

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
    not_lot_name_ids = fields.Char("Forbidden lot names", help="Forbidden lot names, splitted by ', '")

    def write(self, vals):
        if 'not_lot_names_ids' in vals:
            #Elimino espacios
            vals['not_lot_name_ids'] = vals['not_lot_name_ids'].replace(', ', ',').replace(' ,', ',')
        res = super().write(vals)
        if len(self) == 1:
            fields = self.compute_not_lot_name_ids_fields()
            if any(f in vals for f in fields):
                self.not_lot_name_ids = self._compute_not_lot_name_ids()
        return res

    def compute_not_lot_name_ids_fields(self):
        return ['default_code', 'barcode']

    def _compute_not_lot_name_ids(self):
        if self.not_lot_name_ids:
            # Elimino espacios
            not_lot_names_ids = self.not_lot_name_ids.split(",")
        else:
            not_lot_names_ids = []
        for f in self.compute_not_lot_name_ids_fields():
            lot = hasattr(self, f) and getattr(self, f)
            if lot:
                lot = lot.strip()
                if lot not in not_lot_names_ids:
                    not_lot_names_ids.append(lot)
        # Genero elimiando duplicados
        return ','.join(x for x in list(set(not_lot_names_ids)))

    def compute_not_lot_name_ids(self):
        for product in self:
            product.not_lot_name_ids = product._compute_not_lot_name_ids()

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

    # Esta función devuelve los nº de serie  disponibles en una ubicación para x artículo(s)
    def get_serial_domain(self, location_id=False, lot_names=[], all_x_prod=False):
        n_prod = len(self)
        if not n_prod:
            domain = []
        elif n_prod == 1:
            domain = [('product_id', '=', self.id)]
        else:
            domain = [('product_id', 'in', self.ids)]
        if lot_names:
            domain = expression.AND([domain, [("name", "in", lot_names)]])
        if all_x_prod:
            #Devuelvo todos los del producto
            return domain

        if not location_id:
            location_id = self.env.user.get_lot_stock_id()
        domain = expression.AND([domain, [("location_id", '=', location_id.id)]])
        return domain

    #sanitize_lot_names
    def sanitize_lot_names(self, lot_names, apply_regexp=True):
        warning = ''
        if not lot_names:
            return [], warning
        # Si lot_names es una cadena: Reemplazo los . y las , por retorno de carro y separo por lineas para hacer una lista
        if type(lot_names) is str:
            lot_names = re.sub(r"[,.\t\r\n]", ";", lot_names).split(";")
            # for signo in TO_REPLACE:
            #     lot_names = lot_names.replace(signo, ";")

            # Lo convierto a lista
            

        # Si no es una lista fallo
        if not (type(lot_names) is list):
            _logger.info("%s no es una lista" % lot_names)
            raise ValidationError(_("Values in unknown format"))
        # print(lot_names)
        # CONVIERTO A MAYUSCULAS?
        if self.env.user.company_id.serial_to_upper_case:
            if lot_names:
                lot_names = [x.upper() for x in lot_names]

        # Elimino duplicados de la lista
        set_list = set(lot_names)
        # Elimino vacios
        lot_names = list(set_list - {''})
        if not self:
            #Si no envía producto, salgo aquí, solo limpia la lista
            return lot_names, warning

        not_lot_names = []
        # Miro si tengo que aplicar Expresiones regulares. Lo normal es que si

        apply_regexp = self.reg_exp and (apply_regexp or 'apply_regexp' in self._context and self._context['apply_regexp'])


        if self._context.get('picking_id', False):
            other_moves = self._context['picking_id'].move_line_ids.filtered(lambda x: x.product_id == self)
            if self._context.get('move_line_id', False):
                other_moves = other_moves - self._context['move_line_id']
            # ademas, para evitar los repetidos y ya leidos en ese albarán, aunque en otras líneas
            if other_moves:
                not_lot_names += other_moves.mapped('serial_ids.name')

        res = []
        for lot in lot_names:
            lot = lot.strip()
            if lot is None:
                continue
            if len(lot) < 3:
                msg = _('%s invalid: <3 caracter'%lot)
                _logger.info(msg)
                warning = "{}\n{}".format(warning,msg)
                continue
            if self.not_lot_name_ids and lot in self.not_lot_name_ids:
                msg = _('%s invalid: Forbidden'%lot)
                _logger.info(msg)
                warning = "{}\n{}".format(warning,msg)
                continue
            if lot in not_lot_names:
                msg = _('%s invalid: In same pick'%lot)
                _logger.info(msg)
                warning = "{}\n{}".format(warning,msg)
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

            if apply_regexp:
                if not re.match('%s' % self.reg_exp, lot):  # , flags=re.IGNORECASE)
                    msg = _('%s Regexp: %s'%(lot, self.reg_exp))
                    _logger.info(msg)
                    warning = "{}\n{}".format(warning,msg)
                    continue
            res.append(lot)
        return sorted(res), warning
