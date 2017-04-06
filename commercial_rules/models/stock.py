# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from openerp import models, api, exceptions, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_invoice_create(self, journal_id, group=False,
                              type='out_invoice'):
        """
        """
        res = super(StockPicking, self).\
            action_invoice_create(journal_id, group=group, type=type)
        for inv in self.env['account.invoice'].browse(res):
            to_create_promo = {}
            for l in inv.invoice_line:
                domain = [('invoice_lines', 'in', [l.id])]
                sale_line = self.env['sale.order.line'].search(domain)
                if sale_line:
                    domain = [
                        ('order_id', '=', sale_line.order_id.id),
                        ('promotion_line', '=', True),
                        ('orig_line_ids', 'in', [sale_line.id])
                    ]
                    promo_lines = self.env['sale.order.line'].search(domain)
                    for pl in promo_lines:
                        if pl not in to_create_promo:
                            to_create_promo[pl] = []
                        to_create_promo[pl].append(l)
            for promo in to_create_promo:
                qty = sum([x.quantity for x in to_create_promo[promo]])
                account_id = promo.product_id.property_account_income.id
                if not account_id:
                    account_id = promo.product_id.categ_id.\
                        property_account_income_categ.id
                    if not account_id:
                        raise exceptions.except_orm(
                            _('Error!'),
                            _('Please define income account for this \
                              product: "%s" (id:%d).') %
                            (promo.product_id.name, promo.product_id.id,))
                    fpos = promo.order_id.fiscal_position or False
                    if fpos:
                        account_id = fpos.map_account(account_id)
                vals = {
                    'name': promo.name,
                    'sequence': promo.sequence,
                    'origin': promo.order_id.name,
                    'account_id': account_id,
                    'price_unit': promo.price_unit,
                    'quantity': qty,
                    'uos_id': promo.product_uom.id,
                    'product_id': promo.product_id.id,
                    'invoice_line_tax_id': [(6, 0,
                                            [x.id for x in promo.tax_id])],
                    'invoice_id': inv.id
                }
                self.env['account.invoice.line'].create(vals)
        return res
