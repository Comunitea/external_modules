# -*- coding: utf-8 -*-
# © 2009 Albert Cervera i Areny <http://www.nan-tic.com)>
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# © 2011 Pexego Sistemas Informáticos.
#        Alberto Luengo Cabanillas <alberto@pexego.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api


class OpenRiskWindow(models.TransientModel):
    """ Open Risk Window and show Partner relative information """

    _name = 'open.risk.window'
    _description = "Partner's risk information"

    unpayed_amount = fields.Float('Expired Unpaid Payments', readonly="True")
    pending_amount = fields.Float('Unexpired Unpaid Payments', readonly="True")
    circulating_amount = fields.Float('Circulating amount', readonly="True")
    draft_invoices_amount = fields.Float('Draft Invoices', readonly="True")
    pending_orders_amount = fields.Float('Uninvoiced Orders', readonly="True")
    total_debt = fields.Float('Total Debt', readonly="True")
    credit_limit = fields.Float('Credit Limit', readonly="True")
    available_risk = fields.Float('Available Credit', readonly="True")
    total_risk_percent = fields.Float('Credit Usage (%)', readonly="True")

    @api.model
    def default_get(self, fields):
        res = super(OpenRiskWindow, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            partner = self.env['res.partner'].browse(active_id)
            res.update({
                'unpayed_amount': partner.unpayed_amount,
                'pending_amount': partner.pending_amount,
                'draft_invoices_amount': partner.draft_invoices_amount,
                'pending_orders_amount': partner.pending_orders_amount,
                'total_debt': partner.total_debt,
                'credit_limit': partner.credit_limit,
                'available_risk': partner.available_risk,
                'total_risk_percent': partner.total_risk_percent,
                'circulating_amount': partner.circulating_amount,
            })
        return res
