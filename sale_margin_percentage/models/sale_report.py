# -*- coding: utf-8 -*-
# © 2016 Comunitea Servicios Tecnológicos (<http://www.comunitea.com>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from openerp.osv import fields, osv
from openerp import tools


class SaleReport(osv.osv):
    _inherit = "sale.report"

    _columns = {
        'benefit': fields.float('Benefit', readonly=True),
        'cost_price': fields.float('Cost Price', readonly=True)
    }

    def _select(self):
        select_str = super(SaleReport, self)._select()
        this_str = \
            """,sum(l.product_uom_qty * l.price_unit * (100.0-l.discount) /
             100.0) - sum(l.purchase_price*l.product_uom_qty)
            as benefit, sum(l.purchase_price*l.product_uom_qty)
            as cost_price"""
        return select_str + this_str

    def init(self, cr):
        # self._table = sale_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(),
                    self._group_by()))
