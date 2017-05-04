# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def ts_get_grid_structure(self, template_id):
        res = {}
        template_obj = self.browse(template_id)
        column_attrs = [{'id': 1, 'name': 'S'}, {'id': 2, 'name': 'M'}, {'id': 3, 'name': 'L'}]
        row_attrs = [{'id': 4, 'name': 'Blanco'}, {'id': 5, 'name': 'Rojo'}]
        str_table = {
            4: {1: {'id': 11, 'stock': '1111111'},
                2: {'id': 12, 'stock': '1111112'},
                3: {'id': 13, 'stock': '1111113'}},
            5: {1: {'id': 21, 'stock': '2222221'},
                2: {'id': 22, 'stock': '2222222'},
                3: {'id': 33, 'stock': '3333333'}}
        }
        res.update({
            'column_attrs': column_attrs,
            'row_attrs': row_attrs,
            'str_table': str_table
        })
        print "********************************************************"
        print "*********** ts_get_grid_structure RESULT: **************"
        print res
        print "********************************************************"
        return res
