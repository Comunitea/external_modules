# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    diff_level = fields.Integer('Location diff level', default=0, help="Location diff level (multiplicator)")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    diff_level = fields.Integer('Picking diff level', compute ='get_diff_level',
                                          help="Picking diff level, sum of move diff level")

    @api.multi
    def get_diff_level(self):
        for pick in self:
            pick.diff_level = sum(move.diff_level for move in pick.move_lines)

    def get__diff_domain(self):
        diff_level = self._context.get('diff_level')
        min_diff = diff_level[0]
        max_diff = diff_level[1]

        sql =" select sm.picking_id from stock_move sm " \
         "join stock_picking_type spt on spt.id = sm.picking_type_id " \
         "where " \
         "sm.picking_id is not null and " \
         "sm.state in ('partially_available', 'assigned') and " \
         "spt.diff_level > 0 group by sm.picking_id having count(sm.id) > {} and count(sm.id) <= {}".format(min_diff, max_diff)
        self._cr.execute(sql)
        res = self._cr.fetchall()
        ids = [x[0] for x in res]
        sql_domain = [('id', 'in', ids)]
        return sql_domain

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'diff_level' in self._context:
            domain += self.get__diff_domain()
        return super(StockPicking, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                      orderby=orderby, lazy=lazy)

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if 'diff_level' in self._context:
            args += self.get__diff_domain()
        return super(StockPicking, self)._search(args, offset=offset, limit=limit, order=order, count=count,
                                                   access_rights_uid=access_rights_uid)