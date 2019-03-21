# © 2018 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    need_packing_list = fields.Boolean('Packing list', default=False)
    packing_list_ids = fields.One2many('stock.packing.list', 'picking_id')


    @api.multi
    def open_stock_move_tree_for_packing(self):
        self.ensure_one()
        model_data = self.env['ir.model.data']
        tree_view = model_data.get_object_reference(
            'delivery_packing_list', 'stock_move_packing_list_tree')
        domain = [('picking_id', '=', self.id)]
        action = self.env.ref(
            'delivery_packing_list.stock_move_packing_list_tree_view_action').read()[0]
        action['views'] = {
            (tree_view and tree_view[1] or False, 'tree')}
        action['domain'] = domain
        action['context'] = {}
        return action


    def fill_sscc(self):
        sscc = self.env['stock.pack.operation.sscc']
        palet = {}
        package = {}
        counter = 0
        ## Creo sscc para todos los palets/packing_list_id

        for move_line in self.move_line_ids:
            if move_line.packing_list_id and move_line.packing_list_id not in palet.keys():
                counter, op_sscc = self.make_sscc(self, move_line, counter, '1', packing_list_id= move_line.packing_list_id)
                palet[move_line.packing_list_id] = op_sscc

        for move_line in self.move_line_ids:
            """
                Crearemos 1 sscc por palet, 1 por bulto completo y
                1 por bulto multiproducto.
            """

            if move_line.result_package_id:
                if move_line.result_package_id not in package.keys():
                    parent = False
                    if move_line.packing_list_id:
                        parent = palet[move_line.packing_list_id].id
                    counter, op_sscc = self.make_sscc(self, move_line, counter, '3', parent=parent, package_id = move_line.result_package_id)
                    package[move_line.result_package_id] = op_sscc
                else:
                    package[move_line.result_package_id].write({'move_line_ids': [(4, move_line.id)]})
            else:
                parent = False
                if move_line.packing_list_id:
                    parent = palet[move_line.packing_list_id].id
                counter, op_sscc = self.make_sscc(self, move_line, counter, '2', parent=parent)



    def make_sscc(self, move_line, counter, type, packing_list_id=False, package_id = False, parent=None):

        """Método con el que se calcula el sscc a partir de
        1 + aecoc + 4 digitos num albaran + secuencia 2 digitos + 1 checksum
        para escribir en el name del paquete"""
        self.ensure_one()
        sscc = self.env['stock.move.line.sscc']

        domain = [('picking_id', '=', self.id)]
        if sscc.search(domain):
            raise  ValidationError (_('Error. This pick has sscc.'))

        picking_name = self.name.split('\\')[-1][-4:]
        first_num = int(self.name.split('\\')[-1][:1])
        sequence = str(counter).zfill(2)
        if counter > 99:
            first_num += 5
            first_num += int(str(counter)[0])
            sequence = str(counter)[1:].zfill(2)
        aecoc = self.env.user.company_id.aecoc_code
        counter += 1
        sscc = str(sscc._checksum(str(first_num) + aecoc + picking_name + sequence))

        sscc_vals = {'name': sscc,
                     'type': type,
                     'picking_id': self.id,
                     'move_line_ids': [(6, 0, [move_line.id])], 'parent': parent}

        if type == '1' and packing_list_id:
            sscc_vals['packing_list_id'] = packing_list_id.id
        if type == '3' and package_id:
            sscc_vals['package_id'] = package_id.id

        op_sscc = sscc.create(sscc_vals)
        if op_sscc.package_id:
            package_id.sscc_id = op_sscc
        if op_sscc.packing_list_id:
            packing_list_id.sscc_id = op_sscc

        return counter, op_sscc