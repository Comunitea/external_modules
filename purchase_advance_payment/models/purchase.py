# Copyright 2019 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    @api.multi
    def _get_amount_residual(self):
        for purchase in self:
            advance_amount = 0.0
            for line in purchase.account_payment_ids:
                if line.state != 'draft':
                    advance_amount += line.amount
            purchase.amount_resisual = purchase.amount_total - advance_amount

    @api.multi
    def _get_payment_move_line_ids(self):
        for purchase in self:
            purchase.payment_line_ids = purchase.account_payment_ids.\
                mapped('move_line_ids').\
                filtered(lambda x: x.account_id.internal_type == 'payable')

    account_payment_ids = fields.One2many('account.payment', 'purchase_id',
                                          string="Pay purchase advanced",
                                          readonly=True)
    amount_resisual = fields.Float('Residual amount', readonly=True,
                                   compute="_get_amount_residual")
    payment_line_ids = fields.Many2many('account.move.line',
                                        string="Payment move lines",
                                        compute="_get_payment_move_line_ids")
