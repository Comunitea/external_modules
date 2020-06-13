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


class SaleOrderLineMapper(Component):
    _inherit = "prestashop.sale.order.line.mapper"

    @mapping
    def tax_id(self, record):
        taxes = (
            record.get("associations", {})
            .get("taxes", {})
            .get(self.backend_record.get_version_ps_key("tax"), [])
        )
        if not isinstance(taxes, list):
            taxes = [taxes]
        result = self.env["account.tax"].browse()
        for ps_tax in taxes:
            result |= self._find_tax(ps_tax["id"])
        if result:
            return {"tax_id": [(6, 0, result.ids)]}
