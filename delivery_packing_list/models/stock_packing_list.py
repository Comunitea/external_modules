# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError
class StockPackingType(models.Model):
    _name = "stock.packing.type"

    """
    Tipo de empaquetado:
    - Amazon EDI
    - Corte Inglés EDI
    Cada uno puede tener sus tipos de paquete concretos
    """
    name = fields.Char(models.Model)


class StockPackingTypeList(models.Model):

    _name = "stock.packing.type.list"

    """ 
    Tipos de paquete para cada tipo
    """
    name = fields.Char('Name')
    code = fields.Char('Code')
    packing_type_id = fields.Many2one('stock.packing.type', string="Tipo de empaquetado")

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    sscc_id = fields.Many2one('stock.move.line.sscc', 'SSCC')

class StockPackOperationSscc(models.Model):

    _name = 'stock.move.line.sscc'

    name = fields.Char()
    type = fields.Selection(
        (('1', 'Palet'), ('2', 'Complete'), ('3', 'Paquete')))
    parent = fields.Many2one('stock.move.line.sscc')
    move_line_ids = fields.Many2many(
        'stock.move.line', 'operation_sscc_rel', 'sscc_id', 'move_line_id')
    packing_list_id = fields.Many2one('stock.quant.package', 'Packing')
    package_id = fields.Many2one('stock.quant.package', 'Package')
    child_ids = fields.One2many('stock.move.line.sscc', 'parent')

    def _checksum(self, sscc):
        """Devuelve el sscc pasado mas un dígito calculado"""
        iSum = 0
        for i in range(len(sscc) - 1, -1, -2):
            iSum += int(sscc[i])
        iSum *= 3
        for i in range(len(sscc) - 2, -1, -2):
            iSum += int(sscc[i])

        iCheckSum = (10 - (iSum % 10)) % 10

        return "%s%s" % (sscc, iCheckSum)


class StockPackingList(models.Model):

    _name = 'stock.packing.list'
    _order = 'name'

    ##PALET S O UNIDAD LOGISTICA PALET/CAJA/PAQUETE
    @api.multi
    @api.depends('stock_move_ids')
    def _compute_weight(self):

        for pack in self:
            weight = 0.00
            for ml in pack.stock_move_ids:
                weight += ml.product_uom._compute_quantity(ml.quantity_done, ml.product_id.uom_id) * ml.product_id.weight
            pack.weight = weight

    def _default_uom(self):
        uom_categ_id = self.env.ref('product.product_uom_categ_kgm').id
        return self.env['product.uom'].search([('category_id', '=', uom_categ_id), ('factor', '=', 1)], limit=1)

    name = fields.Char('Number', store=True, readonly=1)
    weight = fields.Float("Weight", compute='_compute_weight')
    weight_uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly="1", help="Unit of measurement for Weight", default=_default_uom)
    volume = fields.FLoat('Volume', compute='_compute_weight')
    packing_type_id = fields.Many2one('stock.packing.type', "Packing list type")
    packing_type_list_id = fields.Many2one('stock.packing.type.list', "Packing type")
    picking_id = fields.Many2one('stock.picking', 'Parent picking')
    stock_move_ids = fields.One2many('stock.move', 'packing_list_id', string='Contents')
    stock_move_line_ids = fields.One2many('stock.move.line', 'packing_list_id', string='Contents')
    sscc_id = fields.Many2one('stock.move.line.sscc', 'SSCC')


    @api.model
    def default_get(self, fields):
        res = super(StockPackingList, self).default_get(fields)
        domain = [('picking_id', '=', res['picking_id'])]
        count = self.env['stock.packing.list'].search_count(domain)
        res['name'] = str(count+1).zfill(2)
        return res
