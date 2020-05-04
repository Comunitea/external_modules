# © 2020 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class SaleOrderImportMapper(Component):
    _inherit = "prestashop.sale.order.mapper"

    @mapping
    def prestashop_state(self, record):
        ps_state_id = record["current_state"]
        state = self.binder_for("prestashop.sale.order.state").to_internal(
            ps_state_id, unwrap=1
        )
        return {"prestashop_state": state.id}
