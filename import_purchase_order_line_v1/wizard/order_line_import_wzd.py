# © 2016 Comunitea - Kiko Sánchez <kiko@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, _
from odoo.exceptions import UserError
import xlrd
import base64

import logging
_logger = logging.getLogger(__name__)

template_ids = []

class PurchaseOrderLineImportWzd(models.TransientModel):

    _name = 'purchase.order.line.import.wzd'

    def get_default_partner(self):
        domain = [('ref', '=', 'import_purchase_order')]
        partner_id = self.env['res.partner'].search(domain, limit=1)
        return partner_id

    def get_default_product(self):
        domain = [('default_code', '=', 'import_purchase_order')]
        product_id = self.env['product.product'].search(domain, limit=1)
        return product_id

    name = fields.Char('Importation name')
    partner_id = fields.Many2one('res.partner', string='Customer', default=get_default_partner)
    create_product = fields.Boolean("Create product if not exist", default=False)
    file = fields.Binary(string='File', required=True)
    filename = fields.Char(string='Filename')

    def _parse_row_vals(self, row, idx):
        """
        Albaran
        DocDate
        Pedido
        Articulo
        Nombre
        Quantity
        Price
        Currency
        DiscPrcnt
        LineTotal
        """
        res = {
            'albaran': row[0],
            'date': row[1],
            'origin': row[2],
            'default_code': row[3],
            'name': row[4],
            'qty': row[5],
            'price_unit': row[6],
            'currency': row[7],
            'discount': row[8],
            'total': row[9],
        }

        # Check mandatory values setted
        if not row[2]:
            raise UserError(
                _('Missing product in row %s ') % str(idx))
        return res

    def get_date(self, date):
        """21/02/19"""
        seconds = (date - 25569) * 86400.0
        date = fields.datetime.utcfromtimestamp(seconds)
        return date

    def get_str_from_row(self, val):
        try:
            res = str(int(val))
        except:
            res = str(val)
        return res

    def get_double_from_row(self, val):
        try:
            res = val.replace(',', '.')
            res = round(res, 4)
        except:
            res = 0.000
        return res

    def _get_product(self, row_vals):
        default_code = self.get_str_from_row(row_vals['default_code'])
        domain = [('default_code', '=', default_code)]
        product = self.env['product.product'].search(domain, limit=1)
        if not product and self.create_product:
            vals = {
                'default_code': default_code,
                'type': 'product',
                'name': row_vals['name'],
                'standard_price': row_vals['price_unit']}
            print (vals)
            product = self.env['product.product'].create(vals)
            _logger.info(_('CREATED PRODUCT %s / %s') % (default_code, product.display_name))
        return product

    def _create_line(self, row_vals, purchase_order, idx):
        product = self._get_product(row_vals)
        name = '[{}] {}'.format(row_vals['default_code'], row_vals['name'])
        if not product:
            message = "No se ha encontrado el artículo {} en la línea {}".format(name, idx)
            purchase_order.message_post(body=message)
            return False

        vals = {
            'product_id': product.id,
            'product_uom': product.uom_id.id,
            'product_qty': row_vals['qty'],
            'order_id': purchase_order.id,
            'company_id': self.env.user.company_id.id
            }

        order_line = self.env['purchase.order.line'].new(vals)
        order_line.onchange_product_id()
        order_line.name = name
        order_line.price_unit = row_vals['price_unit']
        #order_line.discount = row_vals['discount']
        order_line.product_qty = row_vals['qty']
        order_line._onchange_quantity()
        order_line_vals = order_line._convert_to_write(
            order_line._cache)

        return purchase_order.order_line.browse().create(order_line_vals)



    def _create_order(self, row_vals):

        origin = self.get_str_from_row(row_vals['origin'])
        vals = {'origin': origin,
                'partner_id': self.partner_id.id,
                'company_id': self.env.user.company_id.id,
                'date_order': self.get_date(row_vals['date'])}
        order = self.env['purchase.order'].new(vals)
        order.onchange_partner_id()
        order_vals = order._convert_to_write(order._cache)
        new_order = self.env['purchase.order'].create(order_vals)
        return new_order


    def _get_existing_purchase_order(self, row_vals, idx):
        order = self.get_str_from_row(row_vals['origin'])
        domain = [('origin', '=', order)]
        order = self.env['purchase.order'].search(domain, limit=1)
        if not order:
            order = self._create_order(row_vals)
        return order


    def import_order(self):
        self.ensure_one()
        _logger.info(_('STARTING PURCHASE IMPORTATION'))

        file = base64.b64decode(self.file)
        book = xlrd.open_workbook(file_contents=file)
        sh = book.sheet_by_index(0)
        idx = 1
        order_ids = []
        for nline in range(1, sh.nrows):
            idx += 1
            row = sh.row_values(nline)
            if row[0]:
                row_vals = self._parse_row_vals(row, idx)
                if row_vals['default_code']:
                    order = self._get_existing_purchase_order(row_vals, idx)
                    if order:
                        if not order in order_ids:
                            order_ids.append(order)
                        self._create_line(row_vals, order, idx)

                    _logger.info(_('IMPORTED LINE %s / %s') % (idx, sh.nrows - 1))

        return self.action_view_products(order_ids)

    def action_view_products(self, order_ids):
        self.ensure_one()
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['domain'] = [('id', 'in', [x.id for x in order_ids])]
        return action

