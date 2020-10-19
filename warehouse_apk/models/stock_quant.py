# -*- coding: utf-8 -*-


from odoo import api, models, fields
from odoo.osv import expression
import pprint


class StockQuant(models.Model):

    _inherit = ['info.apk', 'stock.quant']
    _name = 'stock.quant'

    @api.model
    def _gather_apk(self, values):
        location_id = values.get('location_id', 13)
        product_id = values.get('product_id', False)
        folded = values.get('folded', False)
        show_location = False
        filter = values.get('filter', False)
        if filter:
            if filter['location_id']:
                location_id = filter['location_id']
            if filter['product_id']:
                product_id = filter['product_id']

        if location_id:
            if self.env['stock.location'].browse(location_id).child_ids:
                show_location = True
        if product_id:
            where_product = ' and pp.id = {} ' .format(product_id)
        else:
            where_product = ''
        lot_id = values.get('lot_id', False)
        if lot_id:
            where_lot = ' and pp.id = {} '.format(lot_id)
        else:
            where_lot = ''
        package_id = values.get('package_id', False)
        owner_id = values.get('owner_id', False)
        strict = values.get('strict', False)
        quant_ids = []
        sql = "" \
              "select pp.id as product_id, pp.default_code, pt.name, pt.tracking, " \
              "sl.id as location_id, sl.name as loc_name, sl.barcode as loc_barcode , " \
              "spl.id as lot_id, spl.name as lot_name, " \
              "sum(sq.quantity), sum(sq.reserved_quantity), " \
              "pp.wh_code " \
              "from stock_quant sq " \
              "join stock_location sl on sl.id = sq.location_id " \
              "join product_product pp on pp.id = sq.product_id " \
              "join product_template pt on pt.id = pp.product_tmpl_id " \
              "left join stock_production_lot spl on spl.id = sq.lot_id " \
              "where sl.parent_path ilike '%/{}/%' {} " \
              "group by pp.id, pp.default_code, pt.tracking, pt.name, sl.name, sl.barcode, sl.removal_priority, spl.id, spl.name, sl.id, pp.wh_code " \
              "order by sl.removal_priority asc".format(location_id, where_product, where_lot)

        self._cr.execute(sql)
        res_sql = self._cr.fetchall()
        product_index = {}
        index = 0
        p_index = 0
        res = []

        for quant in res_sql:
            tracking = quant[3]
            create_product = create_loc = create_lot = True
            code = quant[1]
            for product in res:
                if code == product['default_code']:
                    create_product = False
                    break
                p_index += 1
            if create_product:
                product = {'id': quant[0],
                           'folded': False,
                           'default_code': quant[1],
                           'name': quant[2] or quant[1],
                           'wh_code': quant[11] or quant[1],
                           'tracking': quant[3],
                           'location_ids': [],
                           'quantity': 0,
                           'reserved_quantity': 0}

            loc_index = 0
            if not create_product:
                for location in product['location_ids']:
                    if location['barcode'] == quant[6]:
                        create_loc = False
                        break
                    loc_index += 1
            if create_loc:
                location = {'id': quant[4],
                            'folded': True,
                            'show_location': show_location,
                            'name': quant[5] ,
                            'barcode': quant[6],
                            'lot_ids': [],
                            'quantity': 0,
                            'reserved_quantity': 0}
                ## product['location_ids'].append(location)

            lot_index = 0
            if tracking != 'none':
                ## Hay lote
                if not create_loc:
                    for lot in location['lot_ids']:
                        if lot['name'] == quant[8] or False:
                            create_lot = False
                            break
                        lot_index += 1
                if create_lot:
                    lot = {'id': quant[7] or False,
                           'name': quant[8] or False,
                           'quantity': quant[9],
                           'reserved_quantity': quant[10]}
                    #location['lot_ids'].append(lot)
                else:
                    location['lot_ids'][lot_index]['quantity'] += quant[9]
                    location['lot_ids'][lot_index]['reserved_quantity'] += quant[10]
            else:
                create_lot = False

            location['quantity'] += quant[9]
            location['reserved_quantity'] += quant[10]
            product['quantity'] += quant[9]
            product['reserved_quantity'] += quant[10]
            if create_lot:
                location['lot_ids'].append(lot)
            if create_loc:
                product['location_ids'].append(location)
            if create_product:
                res.append(product)
        ##pprint.PrettyPrinter(indent=2).pprint(res)
        return res
