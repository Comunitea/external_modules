
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _
from odoo.exceptions import UserError
import xlrd
import base64

import logging
_logger = logging.getLogger(__name__)

# Global variable to store the new created templates
template_ids = []


class StockImportWzd(models.TransientModel):

    _name = 'stock.import.wzd'

    name = fields.Char('Importation name', required=True)
    picking_id = fields.Many2one('stock.picking')
    file = fields.Binary(string='File', required=True)
    filename = fields.Char(string='Filename')

    def _parse_row_vals(self, row, idx):
        res = {
            'barcode': row[1],
            'articulo': row[2],
            'cantidad': row[3],
            # 'ref': row[4],
        }


        return res

    def _create_xml_id(self, xml_id, res_id, model):
        virual_module_name = 'PT' if model == 'product.template' else 'PP'
        self._cr.execute(
            'INSERT INTO ir_model_data (module, name, res_id, model) \
            VALUES (%s, %s, %s, %s)',
                        (virual_module_name, xml_id, res_id, model))


    def _get_product_id(self, barcode):

        domain = [('barcode', '=', barcode)]
        product_id = self.env['product.product'].search(domain, limit=1)
        if not product_id:
            ref= barcode[2:11]
            print ("No encuentro el codigo de barras: {}".format(barcode))
            domain = [('default_code', '=', ref)]
            product_id = self.env['product.product'].search(domain, limit=1)
            if not product_id:
                print("No encuentro la referencia: {}".format(ref))
        return product_id

    # def _get_product_id_by_ref(self, ref):
    #     domain = [('default_code', '=', ref)]
    #     product_id = self.env['product.product'].search(domain, limit=1)
    #     if not product_id:
    #         print("No encuentro la referencia: {}".format(ref))
    #     return product_id

    def _get_move_line(self, vals, picking_id):

        product_id = self._get_product_id(str(int(vals['barcode'])))
        # if vals.get('ref'):
        #     product_id = self._get_product_id_by_ref(vals['ref'])
        # else:
        #     product_id = self._get_product_id(str(int(vals['barcode'])))
        if not product_id:
            picking_id.message_post(body='No se ha encontrado nada {}'.format(vals))
        else:
            move_vals = {'product_id': product_id.id,
                         'name': vals['articulo'],
                         'picking_id': self.picking_id.id,
                         'location_id': self.picking_id.location_id.id,
                         'location_dest_id': self.picking_id.location_dest_id.id,
                         'product_uom_qty': vals['cantidad'],}


            move = self.env['stock.move'].new(move_vals)
            move.onchange_product_id()
            move_values = move._convert_to_write(move._cache)

            move.create(move_values)
            return product_id

    def import_products(self):
        self.ensure_one()
        _logger.info(_('STARTING PRODUCT IMPORTATION'))

        # get the first worksheet
        file = base64.b64decode(self.file)
        book = xlrd.open_workbook(file_contents=file)
        sh = book.sheet_by_index(0)
        created_product_ids = []
        idx = 1
        self.picking_id.origin = 'IMPORTACIÓN'
        for nline in range(idx, sh.nrows):
            idx += 1
            row = sh.row_values(nline)
            row_vals = self._parse_row_vals(row, idx)
            if row_vals['barcode']:
                product_id = self._get_move_line(row_vals, self.picking_id)
                if product_id:
                    _logger.info(_('Importado movimeinto:  %s (%s / %s)') % (product_id.display_name, idx, sh.nrows - 1))
                    created_product_ids.append(product_id.id)
                else:
                    _logger.info(_('Error en línea %s (%s / %s)') % (idx, idx, sh.nrows - 1))
        return self.action_view_products(created_product_ids)

    def action_view_products(self, product_ids):
        self.ensure_one()
        action = self.env.ref(
            'product.product_normal_action_sell').read()[0]
        action['domain'] = [('id', 'in', product_ids)]
        return action
