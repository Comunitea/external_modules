# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

class ProductProduct(models.Model):

    _inherit = 'product.product'


    @api.multi
    def act_fixed_to_stock(self):
        ##PONER EN LOS PUTAWAYS EL LA UBICACION CON STOCK SI

        sql = "select sum(quantity) as qty, sl.id as fixed_location_id, product_id as product_id, pp.product_tmpl_id as product_tmpl_id from stock_quant sq " \
              "join stock_location sl on sl.id = sq.location_id " \
              "join product_product pp  on sq.product_id = pp.id " \
              "where sl.usage='internal' and sl.posx>0 and sq.quantity > 0 " \
              "group by pp.product_tmpl_id, product_id, sq.company_id, sq.location_id, sl.id " \
              "order by product_id desc, sum(quantity) desc " \

        self._cr.execute(sql)
        sp = self.env['stock.product.putaway.strategy']
        result = self._cr.fetchall()
        total = len(result)
        cont=0
        for res in result:
            cont+=1
            if not self.browse(res[2]).product_putaway_ids:
                vals = {'putaway_id': 1, 'product_tmpl_id': res[3], 'product_product_id': res[2], 'fixed_location_id': res[1]}
                print ("{} de {}: {}".format(cont, total, vals))
                sp.create(vals)


