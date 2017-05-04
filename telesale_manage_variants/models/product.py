# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def ts_get_grid_structure(self, template_id):
        res = {
            'column_attrs': [],
            'row_attrs': [],
            'str_table': {}
        }
        # column_attrs = [{'id': 1, 'name': 'S'}, {'id': 2, 'name': 'M'}, {'id': 3, 'name': 'L'}]
        # row_attrs = [{'id': 4, 'name': 'Blanco'}, {'id': 5, 'name': 'Rojo'}]
        # str_table = {
        #     4: {1: {'id': 11, 'stock': '1111111'},
        #         2: {'id': 12, 'stock': '1111112'},
        #         3: {'id': 13, 'stock': '1111113'}},
        #     5: {1: {'id': 21, 'stock': '2222221'},
        #         2: {'id': 22, 'stock': '2222222'},
        #         3: {'id': 33, 'stock': '3333333'}}
        # }

        template = self.browse(template_id)

        num_attrs = len(template.attribute_line_ids)
        if not template or not (num_attrs > 1):
            return res
        line_x = template.attribute_line_ids[0]
        line_y = False if num_attrs == 1 else template.attribute_line_ids[1]
        for value_x in line_x.value_ids:
            x_attr = {
                'id': value_x.id,
                'name': value_x.name
            }
            res['column_attrs'].append(x_attr)
            res['str_table'][value_x.id] = {}
            for value_y in line_y.value_ids:
                y_attr = {
                    'id': value_y.id,
                    'name': value_y.name
                }
                res['row_attrs'].append(y_attr)
                values = value_x
                if value_y:
                    values += value_y
                product = template.product_variant_ids.filtered(
                    lambda x: not(values - x.attribute_value_ids))[:1]
                
                cell_dic = {
                    'id': product and product.id or 0,
                    'stock': product and product.global_available_stock or 0,
                    'price': product and product.lst_price or 0,
                }
                res['str_table'][value_x.id][value_y.id] = cell_dic
                
        print "********************************************************"
        print "*********** ts_get_grid_structure RESULT: **************"
        import pprint
        print pprint.pprint(res)
        print pprint.pprint(res)
        # print res
        print "********************************************************"
        return res
