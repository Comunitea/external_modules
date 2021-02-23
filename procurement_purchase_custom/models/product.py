import logging

from odoo import api, fields, models, _

from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    twelve_months_ago = fields.Float()
    six_months_ago = fields.Float()
    last_month_ago = fields.Float()
    main_supplier_id = fields.Many2one('res.partner', string='Main Supplier',
                                       compute="_compute_supplier_info",
                                       store=True)
    supplier_min_qty = fields.Float(string='Supplier Min Qty',
                                    compute="_compute_supplier_info")
    supplier_price = fields.Float(string='Supplier Price',
                                  compute="_compute_supplier_info")
    supplier_delay = fields.Integer(string='Supplier Delay',
                                    compute="_compute_supplier_info")
    purchase_qty = fields.Float(string='Purchase Qty',
                                compute="_compute_supplier_info",
                                readonly=True)
    actual_po_id = fields.Many2one('purchase.order',
                                   string='Actual Purchase Order',
                                   compute="_compute_supplier_info",
                                   )

    @api.depends('seller_ids', 'seller_ids.name', 'seller_ids.price')
    def _compute_supplier_info(self):
        for product in self:
            if product.seller_ids:
                product.nbr_suppliers = len(product.seller_ids)
                product.supplier_min_qty = product.seller_ids[0].min_qty
                product.supplier_price = product.seller_ids[0].price
                product.supplier_delay = product.seller_ids[0].delay
                product.main_supplier_id = product.seller_ids[0].name
            else:
                product.nbr_suppliers = 0
                product.supplier_min_qty = 0
                product.supplier_price = 0
                product.supplier_delay = 0
                product.main_supplier_id = False
            pol = self.env['purchase.order.line'].search([
                ('product_id', '=', product.id),
                ('state', 'not in', ['purchase', 'cancel', 'done'])
            ])
            if pol:
                product.purchase_qty = sum(pol.mapped("product_qty"))
                product.actual_po_id = pol[0].order_id
                _logger.info('Product Compute Supplier Info for Purchase \
                               Order %s with Purchase Qty %s' % (
                    product.actual_po_id.name, product.purchase_qty)
                )
            else:
                product.purchase_qty = 0
                product.actual_po_id = False
                _logger.info(
                    'Product Compute Supplier Info with NO Order and \
                    NO Purchase Qty'
                )

    @api.model
    def compute_last_sales(self, products=False):
        twelve_months_ago = fields.Datetime.now() + relativedelta.relativedelta(
            months=-12)
        six_months_ago = fields.Datetime.now() + relativedelta.relativedelta(
            months=-6)
        last_month_ago = fields.Datetime.now() + relativedelta.relativedelta(
            months=-1)

        if not products:
            products = self.search([("type", "!=", "service")])
        for product in products:
            sale_lines_12 = self.env["sale.order.line"].search([
                ("product_id", "=", product.id),
                ("order_id.date_order", ">=", twelve_months_ago),
                ("state", "not in", ('draft', 'sent', 'cancel')),
            ])
            sale_lines_6 = self.env["sale.order.line"].search([
                ("product_id", "=", product.id),
                ("order_id.date_order", ">=", six_months_ago),
                ("state", "not in", ('draft', 'sent', 'cancel')),
            ])
            sale_lines_1 = self.env["sale.order.line"].search([
                ("product_id", "=", product.id),
                ("order_id.date_order", ">=", last_month_ago),
                ("state", "not in", ('draft', 'sent', 'cancel')),
            ])
            product.twelve_months_ago = sum(
                sale_lines_12.mapped("product_uom_qty")
            )
            product.six_months_ago = sum(
                sale_lines_6.mapped("product_uom_qty")
            )
            product.last_month_ago = sum(
                sale_lines_1.mapped("product_uom_qty")
            )
            _logger.info('Compute Last Sales for Product %s for 12 Months \
                           with %s, for 6 Months with %s and Last Month with %s'
                          % (product.name, product.twelve_months_ago,
                             product.six_months_ago, product.last_month_ago)
            )

    @api.model
    def _cron_compute_last_sales(self):
        self.compute_last_sales()

    def button_compute_last_sales(self):
        self.compute_last_sales(self)

    def get_unreceived_items(self):
        model_data = self.env["ir.model.data"]
        tree_view = model_data.get_object_reference(
            "procurement_purchase_custom", "purchase_custom_tree"
        )
        search_view = model_data.get_object_reference(
            "procurement_purchase_custom", "purchase_custom_search"
        )
        domain = [("product_id", "=", self.id)]
        value = {}
        for call in self:
            value = {
                "name": _("Purchase Order Lines"),
                "view_type": "form",
                "view_mode": "tree,form",
                "res_model": "purchase.order.line",
                "views": [(tree_view and tree_view[1] or False, "tree")],
                "type": "ir.actions.act_window",
                "domain": domain,
                "search_view_id": search_view and search_view[1] or False,
                "context": {'search_default_in_1_stock': 1},
            }
        return value
