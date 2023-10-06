# © 2019 Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# from odoo.tools.float_utils import float_compare
import logging

from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

LOT_NAMES_TYPES = [
    ("supplier", "Vendor Location"),
    ("view", "View"),
    ("internal", "Internal Location"),
    ("customer", "Customer Location"),
    ("inventory", "Inventory Loss"),
    ("procurement", "Procurement"),
    ("production", "Production"),
    ("transit", "Transit Location"),
]


from odoo import tools
from odoo import api, fields, models


# Este debe ser un objeto temporal, existe mientras se están metiendo serials sin crearlos erroneamente

class VirtualSerial(models.Model):
    _name = 'virtual.serial'

    name = fields.Char('Nº Series', required=True)
    move_line_id = fields.Many2one('stock.move.line', string="Related Move Line")

    _sql_constraints = [
        (
            'code_uniq',
            'UNIQUE(name, move_line_id)',
            'Name must be unique per Move!'
        ),
    ]

    @api.model
    def create(self, values):
        ## Lo hago postgresql directamente por tema de velocidad. La pda está esperando ...
        try:
            if values.get('move_line_id', False) and values.get('name', False):
                sql = "INSERT INTO virtual_serial (id, create_uid, create_date, write_uid, write_date, move_line_id, name, lot_id) VALUES (nextval('virtual_serial_id_seq'), 6, (now() at time zone 'UTC'), 6, (now() at time zone 'UTC'), %d, '%s', (select spl.id from stock_production_lot spl where spl.name = '%s' and product_id = (select product_id from stock_move_line where id = %d))) ON CONFLICT DO nothing  RETURNING id" %(values['move_line_id'], values['name'], values['name'], values['move_line_id'])
                self._cr.execute(sql)
                id = self._cr.fetchone()
                if id:
                    return self.browse(id)
                else:
                    _logger.info("El nombre/movimiento ya existe %s"%(values['name']))
                    return self.env['virtual.serial']
        except:
            _logger.info("Ha ocurrido un error al crear con %s"%(values))
            return self.env['virtual.serial']

    @api.multi
    def convert_to_spl(self, move_line_id, product_id, location_id):
        # Convierte una lista de virtual serial a lotes de odoo
        # Y lo añade a un stock_move_line
        if not product_id.virtual_tracking:
            raise ValidationError(_("%s no tiene tracking virtual"%product_id.display_name))
        domain = [
            ('product_id', '=', product_id.id),
            ('name', 'in', self.mapped('name')),
            '|', ('active', '=', True), ('active', '=', False)]
        serial_ids = self.env['stock.lot'].search(domain)

        id_to_link = []
        values_to_link = []
        for vpl_id in self:
            spl_id = serial_ids.filtered(lambda x: x.name == vpl_id.name)
            if spl_id:
                # Ya existe, por lo que lo añado.
                if not spl_id.active:
                    spl_id.active = True
                id_to_link += [spl_id]
            else:
                # Los tengo que crear.
                values = {
                    'name': vpl_id.name,
                    'product_id': product_id.id,
                    'location_id': location_id.serial_location.id,
                    'real_location_id': location_id.id,
                    'ref': vpl_id.name}
                values_to_link += [values]
        if id_to_link:
            move_line_id.serial_ids = [(4, id) for id in id_to_link]
        if values_to_link:
            move_line_id.serial_ids = [(0, 0, values) for values in values_to_link]

class VirtualLastLoc(models.Model):
    _name = "virtual.last.location"
    _description = "Virtual Serial Last Location"
    _auto = False
    _rec_name = 'lot_id'
    _order = 'date desc'

    @api.model
    def _get_done_states(self):
        return ['sale', 'done', 'paid']

    location_id = fields.Many2one(comodel_name='stock.location', string="Actual Location", readonly=True)
    lot_id = fields.Many2one(comodel_name='stock.lot', string="Virtual Serial", readonly=True)
    product_id = fields.Many2one(comodel_name='product.product', string="Producto", readonly=True)
    date = fields.Datetime('Order Date', readonly=True)

    def _query(self):
        select_ = """
            select
            sml.id as id,
            lmlrel.serial_id as lot_id,
            sml.product_id as product_id,
            sml.date as date,
            sml.location_dest_id as location_id
            from stock_move_line sml
            join serial_id_move_line_id_rel lmlrel on lmlrel.move_line_id = sml.id
            where sml.state = 'done'
        """
        return select_

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

class StockLot(models.Model):
    _inherit = "stock.lot"

    virtual_tracking = fields.Boolean(related='product_id.virtual_tracking')
    location_id = fields.Many2one("stock.location", "Location")
    serial_location_id = fields.Many2one(related="location_id.serial_location", string="Serial Location", store=True)
    move_line_ids = fields.One2many(
        "stock.move.line", compute="_compute_tracking_moves"
    )
    move_ids = fields.One2many("stock.move", compute="_compute_tracking_moves")

    @api.multi
    def unlink(self):
        sql = "select move_line_id from serial_id_move_line_id_rel where serial_id in %s"
        self._cr.execute(sql, [tuple(self.ids)])
        res = self._cr.fetchall()
        if res:
            raise ValidationError (_('Serial numbers used in any '))
        return super().unlink()

    @api.multi
    def _compute_tracking_moves(self):
        for lot in self:
            domain = ['|', ('lot_id', '=', lot.id), ("serial_ids", "in", lot.id)]
            lot.move_line_ids = self.env["stock.move.line"].search(domain, order="date asc")
            lot.move_ids = lot.move_line_ids.mapped("move_id")

    def show_tracking_move_ids(self):
        action = self.env.ref(
            'stock.stock_move_line_action').read([])[0]
        action['domain'] = [('id', 'in', self.move_line_ids.ids)]
        action['context'] = {}
        return action

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # Añado el filtro available para ver si hay stock para esos lotes ????
        if self._context.get("available", False):
            # V12
            # stock_location = self._context.get('stock_location')
            # if not stock_location:
            #     stock_location = self.env.ref('stock.stock_location_stock')
            # d1 = self.env['product.product'].get_serial_domain(location_id=stock_location.id)
            # d1 = [("serial_location_id", "=", stock_location.serial_location.id)]
            d1 = [("serial_location_id.usage", "=", 'internal')]
            args = expression.normalize_domain(args)
            args = expression.AND([d1, args])
        res = super().search(args, offset=offset, limit=limit, order=order, count=count)
        return res

    @api.model
    def create(self, vals):
        return super().create(vals)

    def update_real_location_id(self):
        # Script para calcular el la ubicación real por si se descoloca
        if not self:
            self = self.search([])
        for serial in self.sudo().filtered(lambda x: x.virtual_tracking):
            _logger.info("Actualizando {}".format(serial.name))
            domain = [('lot_id', '=', serial.id)]
            vll_id = self.env['virtual.last.location'].search(domain, limit=1)
            if vll_id:
                location_id = serial.location_id
                serial.location_id = vll_id.location_id
                _logger.info(">>>> De {} ({}) a {}".format(location_id.display_name, vll_id.location_id.serial_location.display_name, serial.real_location_id.display_name))

    @api.multi
    def write(self, vals):
        if vals.get("name"):
            if self.env.user.company_id.serial_to_upper_case:
                name = vals.get("name").upper()
                if name != vals.get("name"):
                    vals.update({'name': name, 'ref': name})
        return super().write(vals)

    @api.model
    def create(self, vals):
        
        name = vals.get("name").upper()
        if name != vals.get("name"):
            if self.env.user.company_id.serial_to_upper_case:
                vals.update({'name': name, 'ref': name})
        return super().create(vals)
