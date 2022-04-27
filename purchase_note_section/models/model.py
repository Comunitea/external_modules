# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    @api.depends('order_line.date_planned', 'date_order')
    def _compute_date_planned(self):
        # fix line.date_planned mandatory field
        for order in self:
            min_date = False
            for line in order.order_line:
                if not line.display_type:
                    if not min_date or line.date_planned < min_date:
                        min_date = line.date_planned
            if min_date:
                order.date_planned = min_date
            else:
                order.date_planned = order.date_order

    @api.multi
    def _add_supplier_to_product(self):
        # remove line_note and line_section
        for line in self.order_line:
            # Do not add a contact as a supplier
            partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
            if line.product_id and partner not in line.product_id.seller_ids.mapped('name') and len(
                    line.product_id.seller_ids) <= 10:
                currency = partner.property_purchase_currency_id or self.env.user.company_id.currency_id
                supplierinfo = {
                    'name': partner.id,
                    'sequence': max(
                        line.product_id.seller_ids.mapped('sequence')) + 1 if line.product_id.seller_ids else 1,
                    'product_uom': line.product_uom.id,
                    'min_qty': 0.0,
                    'price': self.currency_id._convert(line.price_unit, currency, line.company_id,
                                                       line.date_order or fields.Date.today(), round=False),
                    'currency_id': currency.id,
                    'delay': 0,
                }
                # In case the order partner is a contact address, a new supplierinfo is created on
                # the parent company. In this case, we keep the product name and code.
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id,
                    quantity=line.product_qty,
                    date=line.order_id.date_order and line.order_id.date_order.date(),
                    uom_id=line.product_uom)
                if seller:
                    supplierinfo['product_name'] = seller.product_name
                    supplierinfo['product_code'] = seller.product_code
                vals = {
                    'seller_ids': [(0, 0, supplierinfo)],
                }
                try:
                    line.product_id.write(vals)
                except AccessError:  # no write access rights -> just ignore
                    break


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _order = "sequence,id"

    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)],
                                 change_default=True, required=False)
    date_planned = fields.Datetime(string='Scheduled Date', index=True, required=False)
    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure', required=False)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    _sql_constraints = [
        ('accountable_required_fields',
         "CHECK(display_type IS NOT NULL OR (product_id IS NOT NULL AND product_uom IS NOT NULL AND date_planned IS NOT NULL))",
         "Missing required fields on accountable purchase order line."),
        ('non_accountable_null_fields',
         "CHECK(display_type IS NULL OR (product_id IS NULL AND price_unit = 0 AND product_uom_qty = 0 AND product_uom IS NULL AND date_planned is NULL))",
         "Forbidden values on non-accountable purchase order line"),
    ]

    @api.multi
    def create(self, values):
        if isinstance(values, list):
            for data in values:
                if data.get('display_type', self.default_get(['display_type'])['display_type']):
                    data.update(product_id=False, price_unit=0, product_uom_qty=0, product_uom=False,
                                date_planned=False)
        else:
            if values.get('display_type', self.default_get(['display_type'])['display_type']):
                values.update(product_id=False, price_unit=0, product_uom_qty=0, product_uom=False, date_planned=False)

        return super(PurchaseOrderLine, self).create(values)

    @api.multi
    def write(self, values):
        if 'display_type' in values and self.filtered(
                lambda line: line.display_type != values.get('display_type')):
            raise UserError(_(
                "You cannot change the type of a purchase order line. "
                "Instead you should delete the current line and create a new line of the proper type."))

        res = super(PurchaseOrderLine, self).write(values)

        return res
