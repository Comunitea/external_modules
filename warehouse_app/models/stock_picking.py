# -*- coding: utf-8 -*-
# Copyright 2017 Comunitea - <comunitea@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    show_in_pda = fields.Boolean("Show in PDA", help="If checked, this picking type will be shown in pda")
    short_name = fields.Char("Short name in PDA", help="Short name to show in PDA")
    need_confirm = fields.Boolean("Need confirm in PDA", help="If checked, this force to process with button after all requeriments done")
    process_from_tree = fields.Boolean("Process from pda tree ops", help="If checked, allow to process op with default values from pick tree ops in pda")


class StockPicking(models.Model):
    _inherit = "stock.picking"


    @api.multi
    def ops_count(self):
        for pick in self:
            if pick.move_line_exists:
                pick.count_ops = len(pick.move_line_ids)
                pick.done_ops = len(pick.move_line_ids.filtered(lambda x: x.pda_done or x.qty_done>0.00))
                pick.remaining_ops = pick.count_ops - pick.done_ops
                pick.ops_str = "{} de {}".format(pick.remaining_ops, pick.count_ops)
            else:
                pick.done_ops = pick.remaining_ops = pick.count_ops = 0
                pick.ops_str = "No operation"

    user_id = fields.Many2one('res.users', 'WH Operator')
    remaining_ops = fields.Integer('Operaciones pendientes', compute = 'ops_count')
    count_ops = fields.Integer('Count operations', compute='ops_count')
    done_ops = fields.Integer('Done operations', compute = 'ops_count')
    remaining_ops = fields.Integer('Remaining operations', compute = 'ops_count')
    ops_str = fields.Char('Operation info', compute = 'ops_count')

    show_in_pda = fields.Boolean(related='picking_type_id.show_in_pda')

    ### ESTAS 2 FUNCIONES SIRVEN PARA RECUPERAR E INSTANCIAR EL PICKING CON EL USUARIO INTERCOMPAÑIA ###
    @api.model
    def get_ic_pick(self, id, message=False):
        pick = self.sudo(self.get_ic_pick_user(id)).browse([id])
        if message:
            pick.message_post(message)
        return pick

    @api.model
    def get_ic_pick_user(self, id=False):
        if not id:
            self.ensure_one()
            id = self.id
        sql = u"select intercompany_user_id from res_company rc where id = (select company_id from stock_picking where id = %s)" % id
        self._cr.execute(sql)
        record = self._cr.fetchall()
        return record and record[0][0] or self.env.user.id

    ## Same as Button validate from pda
    @api.model
    def pda_validate(self, vals):
        id = vals.get('id', False)
        message = "Pda validate by %s" % self.env.user.name
        pick = self.get_ic_pick(id, message)
        ## Pda done = True and qty_done = 0.000
        if not pick.move_line_ids.filtered(lambda x:qty_done >0.00 or x.pda_done):
            res = {'id': False, 'message': 'No operation to validate'}
            return
        for move_line_id in pick.move_line_ids.filtered(lambda x: x.pda_done and x.qty_done==0.00):
            move_line_id.qty_done = move_line_id.product_uom_qty


