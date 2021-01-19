# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models, api, exceptions, _


class PrestashopBackend(models.Model):
    _inherit = "prestashop.backend"

    import_image_type = fields.Selection(
        [("url", "URL"), ("db", "Database")], default="url"
    )
    resize_images = fields.Boolean()
    start_import_date = fields.Datetime()

    product_qty_field = fields.Selection(
        selection_add=[
            ("virtual_stock_conservative", "Stock virtual conservativo")
        ]
    )

    @api.multi
    def synchronize_sale_states(self):
        for backend in self:
            self.env['prestashop.sale.order.state'].import_batch(backend)

    @api.constrains("product_qty_field")
    def check_product_qty_field_dependencies_installed(self):
        for backend in self:
            # we only support stock_available_unreserved module for now.
            # In order to support stock_available_immediately or
            # virtual_available for example, we would need to recompute
            # the prestashop qty at stock move level, it can't work to
            # recompute it only at quant level, like it is done today
            if backend.product_qty_field == "virtual_stock_conservative":
                module = (
                    self.env["ir.module.module"]
                    .sudo()
                    .search(
                        [("name", "=", "product_virtual_stock_conservative")],
                        limit=1,
                    )
                )
                if not module or module.state != "installed":
                    raise exceptions.UserError(
                        _(
                            "In order to choose this option, you have to "
                            "install the module product_virtual_stock_conservative."
                        )
                    )
        return super().check_product_qty_field_dependencies_installed()
