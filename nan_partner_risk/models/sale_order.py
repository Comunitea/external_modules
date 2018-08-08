# -*- coding: utf-8 -*-
# © 2009 Albert Cervera i Areny <http://www.nan-tic.com)>
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# © 2011 Pexego Sistemas Informáticos.
#        Alberto Luengo Cabanillas <alberto@pexego.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_invoiced = fields.Float(compute='_amount_invoiced',
                                   string='Invoiced Amount')
    state = fields.Selection(
        selection_add=[('wait_risk', 'Waiting Risk Approval')])

    @api.multi
    def _amount_invoiced(self):
        for order in self:
            if order.invoiced:
                amount = order.amount_total
            else:
                amount = 0.0
                for line in order.order_line:
                    amount += line.amount_invoiced
            order.amount_invoiced = amount

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Warning when a cash customer is selected
        """
        super(SaleOrder, self).onchange_partner_id()
        result = {}
        if self.partner_id:
            partner = self.partner_id.commercial_partner_id
            if partner.cash:
                result['warning'] = {
                    'title': _('Credit Limit Exceeded'),
                    'message': _('Warning: Credit Limit Exceeded.\n\nThis \
                        partner has a credit limit of %(limit).2f and already \
                        has a debt of %(debt).2f.') % {
                        'limit': partner.credit_limit,
                        'debt': partner.total_debt,
                    }
                }
        return result

    @api.multi
    def draft_to_risk(self):
        return self.write({'state': 'wait_risk'})

    @api.multi
    def risk_to_cancel(self):
        return self.write({'state': 'cancel'})

    @api.multi
    def risk_to_router(self):
        for order in self:
            partner = order.partner_id
            if not partner.credit_limit or \
                    partner.available_risk - order.amount_total >= 0.0:
                order.action_confirm()
            elif partner.credit_limit or \
                    partner.available_risk - order.amount_total < 0.0:
                return self.write({'state': 'wait_risk'})


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    amount_invoiced = fields.Float(compute='_amount_invoiced',
                                   string='Invoiced Amount')

    @api.multi
    def _amount_invoiced(self):

        for line in self:
            # Calculate invoiced amount with taxes included.
            # Note that if a line is only partially invoiced we consider
            # the invoiced amount 0.
            # The problem is we can't easily know if the user changed amounts
            # once the invoice was created
            if line.invoiced:
                line.amount_invoiced = line.price_subtotal + \
                    line._tax_amount()
            else:
                line.amount_invoiced = 0.0

    @api.multi
    def _tax_amount(self, cr, uid, line):
        val = 0.0
        self.ensure_one()
        v = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        for c in line.tax_id.compute_all(
                v, quantity=line.product_uos_qty,
                product=line.product_id,
                partner=line.order_id.partner_id)['taxes']:
            val += c['amount']
        return val
